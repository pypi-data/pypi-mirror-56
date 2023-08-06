import sys, os, logging, requests, copy
import pymysql
import re
import string
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAlert

#https://developers.facebook.com/docs/instagram-api/reference/media/insights

utils = InstagramUtils()
errors = list()

DF = "%Y-%m-%d"

logging.basicConfig(filename='logs/get_business_media_insights.log',level=logging.DEBUG)
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)

def get_path(media_type):
    return {
        'image': 'request_image_path',
        'video': 'request_video_path',
        'carousel_album': 'request_carousel_album_path',
        'story': 'request_story_path',
    }.get(media_type,'')


def request_data(request_path, media_id, access_token):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.%s' % request_path).format(**locals())
  url = '%s%s'%(host,path)
  payload = {'access_token': access_token}
  if utils.has_trace_enabled():
      logging.debug('Url: %s' % url)
  response = requests.get('%s%s'%(host,path), params=payload)
  response_as_json = utils.response_as_json(response)
  if response_as_json == False:
      errors.append(response.text)
  return response_as_json 


def get_media(conn, date_from, date_to):
  media = list()
  try:
    query = utils.from_config("queries.get_media").format(**locals())
    if utils.has_trace_enabled():
        logging.debug("query: %s" % query)
    cursor = conn.cursor(pymysql.cursors.SSCursor)
    cursor.execute(query)
    users = list()
    while (1):
      row = cursor.fetchone()
      if not row:
        break
      user_id = row[0].decode('UTF-8')
      media_id = row[1].decode('UTF-8')
      media_type = row[2].decode('UTF-8')
      access_token = row[3].decode('UTF-8')
      media.append((user_id, media_id, media_type, access_token))
    cursor.close()
    logging.debug("Added %s media "%(len(media)))
  except:
      cursor.close()
      logging.exception("Error while getting media")
  return media


def parse_and_insert(conn, user_id, media_id, metrics):  
  cursor = conn.cursor()  
  common_fields = {"user_id": user_id,
                   "media_id": media_id,
                   "end_time": date.strftime(date.today()-timedelta(days=1),DF),
                   "fetched_time": str(datetime.utcnow())}
  for item in metrics:
      metric_name = item.get("name")
      metric_value = item.get("values")[0].get("value") 
      fields = {"metric_name": metric_name,
                "metric_value": metric_value}
      fields.update(common_fields)
      logging.debug("insert with fields: %s" % str(fields))
      command = utils.from_config('queries.insert_insights').format(**fields)
      if utils.has_trace_enabled():
          logging.debug("insert command: %s" % command)
      cursor.execute(command)
  conn.commit()
  cursor.close()

  
  # IP 189.216.115.149/32
# def send_alert(alert_text, alert_type, alert_priority):
#   alert = InternalAlert()
#   alert.priority = alert_priority    # {INFO, WARN, SEVERE}
#   alert.type = "IG_FETCH_MEDIA"
#   alert.project = alert_type
#   alert.text = alert_text
#   alert.created_at = int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())*1000
#   body = alert.SerializeToString()
#   url='http://trb-message-exchange-hrd.appspot.com/alert/internal'
#   logging.debug('alert url: %s' % url)
#   logging.debug('alert body: %s...' % body[:250])
#   r = requests.post(url, body)


def process_business_media_insights(conn, user_id, media_id, media_type, access_token):
    path = get_path(media_type)
    if path == '':
        logger.debug('media type unrecognised for %s: %s'%(media_id,media_type))
        return
    response = request_data(path, media_id, access_token)
    if response:
        try:
            parse_and_insert(conn, user_id, media_id, response.get('data'))
        except:
            logging.exception("Error while parsing or inserting")
    
  
def main(args):  
  conf_file = "conf/get_business_media_insights.yaml"
  utils.init(conf_file, True)
  exec_start_time = datetime.now()
  try:    
    conn = utils.get_conn('ig')
    date_from, date_to = utils.get_start_end_str(args, 15)
    media = get_media(conn, date_from, date_to)
    for item in media:
      user_id = item[0]
      media_id = item[1]
      media_type = item[2]
      access_token = item[3]
      process_business_media_insights(conn, user_id, media_id, media_type, access_token)
    conn.close()
  except:
    logging.exception('Error executing script')
  finally:
    logging.info('Total time: %s' % (datetime.now() - exec_start_time))

if __name__ == '__main__':
     main(sys.argv[1:])
