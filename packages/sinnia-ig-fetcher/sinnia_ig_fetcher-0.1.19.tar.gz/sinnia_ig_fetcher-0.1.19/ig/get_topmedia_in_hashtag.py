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

logging.basicConfig(filename='logs/get_topmedia_in_hashtag.log',level=logging.DEBUG)
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)


def request_hashtag_id(user_id, hashtag, access_token):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.request_ht_id_path').format(**locals())
  url = '%s%s'%(host,path)
  payload = {'access_token': access_token}
  if utils.has_trace_enabled():
      logging.debug('Url: %s' % url)
  response = requests.get('%s%s'%(host,path), params=payload)
  response_as_json = utils.response_as_json(response)
  if response_as_json == False:
      errors.append(response.text)
  return response_as_json 


def request_hashtag_media(user_id, access_token, hashtag_id, date_from, date_to):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.request_ht_media_path').format(**locals())
  historic = ''
  if (date_from != None and date_to != None): 
    historic = utils.from_config('graph_api.historic_suffix').format(**locals())
  url = '%s%s%s'%(host,path,historic)
  payload = {'access_token': access_token}
  if utils.has_trace_enabled():
      logging.debug('Url: %s...' % url)
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
    users = list()
    while (1):
      row = cursor.fetchone()
      if not row:
        break
      user_id = row[0].decode('UTF-8')
      hashtag = row[1].decode('UTF-8')
      access_token = row[2].decode('UTF-8')
      users.append((user_id, hashtag, access_token))
      logging.debug("Adding user_id %s"%(user_id))
    cursor.close()
    logging.debug("Added %s users "%(len(users)))
  except:
      logging.exception("Error while getting users")
  return users


def parse_and_insert(conn, user_id, data, hashtag):      
  cursor = conn.cursor()
  for item in data:
      media_url = str(item.get("media_url", ""))
      values = {"id" : str(item["id"]),
                "user_id": 0,
                "created_at": str(datetime.utcnow()), # info not present
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type",'')),
                "caption": str(item.get("caption",'')).replace("'",'"'),
                "url": str(item.get("permalink",'')),
                "likes_count": item.get("like_count",0),
                "comments_count": item.get("comments_count",0),
                "image": media_url}
      command = utils.from_config('queries.insert_media').format(**values)
      if utils.has_trace_enabled():
          logging.debug("insert command: %s" % command)
      cursor.execute(command)
      conn.commit()

      ht_values = {"media_id": str(item["id"]),
                   "hashtag": hashtag,
                   "lower_hashtag": str.lower(hashtag),
                   "created_at": str(datetime.utcnow())}
      ht_command = utils.from_config('queries.insert_ht').format(**ht_values)
      if utils.has_trace_enabled():
          logging.debug("insert_ht command: %s" % ht_command)
      cursor.execute(ht_command)
      conn.commit()
  logging.debug("Inserted %s media for hashtag '%s'" % (len(data), hashtag))
  cursor.close()

  
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


def main(args):  
  conf_file = "conf/get_topmedia_in_hashtag.yaml"
  utils.init(conf_file, True)
  exec_start_time = datetime.now()
  try:
    date_from, date_to = utils.get_start_end_str(args)
    conn = utils.get_conn('ig')
    users = get_users(conn)
    for item in users:
      user_id = item[0]
      hashtag = item[1]
      access_token = item[2]
      id_response = request_hashtag_id(user_id, hashtag, access_token)
      if id_response and id_response["data"]!=None and len(id_response["data"])>0:
          try:
              hashtag_id = id_response["data"][0]["id"]
              response=request_hashtag_media(user_id, access_token, hashtag_id,
                                             date_from, date_to)
              parse_and_insert(conn, user_id, response.get('data'), hashtag)
          except:
              logging.exception("Error while parsing or inserting")
    conn.close()
  except:
    logging.exception('Error executing script')
  finally:
    logging.info('Total time: %s' % (datetime.now() - exec_start_time))

if __name__ == '__main__':
     main(sys.argv[1:])
