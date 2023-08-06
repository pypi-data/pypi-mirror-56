import sys, os, logging, requests, copy
import pymysql
import re
import string
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAlert

utils = InstagramUtils()
errors = list()

SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
TARGET_DF = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(filename='logs/get_business_competitors_media.log',
                    level=logging.DEBUG)
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)


def request_data(user_id, competitor_name, access_token, date_from, date_to):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.request_path').format(**locals())
  historic = ''
  if (date_from != None and date_to != None): 
    historic = utils.from_config('graph_api.historic_suffix').format(**locals())
  url = '%s%s%s'%(host,path,historic)
  payload = {'access_token': access_token}
  if utils.has_trace_enabled():
      logging.debug('Url: %s' % url)
  response = requests.get(url, params=payload)
  response_as_json = utils.response_as_json(response)
  if response_as_json == False:
      errors.append(response.text)
  return response_as_json 


def get_users(conn):
  users = list()
  try:
    query = utils.from_config("queries.get_users")
    cursor = conn.cursor(pymysql.cursors.SSCursor)
    cursor.execute(query)
    while (1):
      row = cursor.fetchone()
      if not row:
        break
      user_id = row[0].decode('UTF-8')
      competitor_name = row[1].decode('UTF-8')
      access_token = row[2].decode('UTF-8')
      users.append((user_id, competitor_name, access_token))
      logging.debug("Adding pair %s, %s"%(user_id, competitor_name))
    cursor.close()
    logging.debug("Added %s pairs "%(len(users)))
  except:
      logging.exception("Error while getting users")
  return users


def parse_and_insert(conn, data):
  competitor_id = data.get("id")
  user_values = {"id": competitor_id,
                 "username": data.get("username"),
                 "media_count": data.get("media_count"),
                 "followers_count": data.get("followers_count"),
                 "follows_count": data.get("follows_count")}
  command = utils.from_config('queries.insert_user').format(**user_values)
  cursor = conn.cursor() 
  logging.debug("insert user command: %s" % command)
  cursor.execute(command)
  conn.commit()
  cursor.close()
  
  cursor = conn.cursor()
  for item in data.get("media").get("data"):
      created_datetime = datetime.strptime(item.get("timestamp")[:19],SOURCE_DF)
      created_at = datetime.strftime(created_datetime, TARGET_DF)
      values = {"id" : str(item.get("id")),
                "user_id": str(competitor_id),
                "created_at": str(created_at),
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type", '')),
                "caption": str(item.get("caption", '')).replace("'",'"'),
                "url": str(item.get("permalink", '')),
                "likes_count": item.get("like_count", 0),
                "comments_count": item.get("comments_count", 0),
                "image": str(item.get("media_url", ''))}
      command = utils.from_config('queries.insert_media').format(**values)
      if utils.has_trace_enabled():
          logging.debug("insert media command: %s" % command)
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

def process (conn, user_id, competitor_name, access_token, date_from = None, date_to = None):
    logging.info("##############################################")
    logging.info("Getting media for %s,%s" % (user_id,competitor_name))
    response = request_data(user_id,competitor_name,access_token,date_from,date_to)
    if response:
        try:
            parse_and_insert(conn, response.get('business_discovery'))
        except:
            logging.exception("Error while parsing or inserting")
            
            
def main(args):  
  conf_file = "conf/get_business_competitors_media.yaml"
  utils.init(conf_file, True)
  exec_start_time = datetime.now()
  try:    
    date_from, date_to = utils.get_start_end_str(args)
    conn = utils.get_conn('ig')
    users = get_users(conn)
    for item in users:
      user_id = item[0]
      competitor_name = item[1]
      access_token = item[2]
      process(conn, user_id, competitor_name, access_token, date_from, date_to)
    conn.close()
  except:
    logging.exception('Error executing script')
  finally:
    logging.info('Total time: %s' % (datetime.now() - exec_start_time))

if __name__ == '__main__':
     main(sys.argv[1:])

     
