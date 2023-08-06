import sys, os, logging, requests, copy
import pymysql
import re
import string
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAlert

# https://developers.facebook.com/docs/instagram-basic-display-api/reference/user/media

utils = InstagramUtils()
errors = list()

SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
TARGET_DF = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(filename='logs/get_user_media.log',level=logging.DEBUG)
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)


def make_user_url(user_id, access_token):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.request_user_path').format(**locals())
  return '%s%s'%(host,path)


def make_media_url(user_id, access_token, date_from, date_to):
  host = utils.from_config('graph_api.host')
  path = utils.from_config('graph_api.request_media_path').format(**locals())
  historic = ''
  if (date_from != None and date_to != None): 
    historic = utils.from_config('graph_api.historic_suffix').format(**locals())
  return '%s%s%s'%(host,path,historic)


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
      access_token = row[1].decode('UTF-8')
      users.append((user_id, access_token))
      logging.debug("Adding user_id %s"%(user_id))
    cursor.close()
    logging.debug("Added %s users "%(len(users)))
  except:
      logging.exception("Error while getting users")
  return users


def parse_and_insert_info(conn, user_id, data):
  if len(data) == 0:
      return
  values = {"id": user_id,
            "username": data.get("username"),
            "account_type": data.get("account_type"),
            "media_count": data.get("media_count")}
  command = utils.from_config('queries.insert_user').format(**values)
  cursor = conn.cursor()
  if utils.has_trace_enabled():
      logging.debug("insert user command: %s" % command)
  cursor.execute(command)
  conn.commit()
  cursor.close()
  return user_id


def parse_and_insert_media(conn, user_id, data, is_story=False):
  if len(data) == 0:
      return  
  cursor = conn.cursor()
  cursor.execute('SET character_set_connection=utf8mb4;')
  for item in data:
      created_datetime = datetime.strptime(item["timestamp"][:19], SOURCE_DF)
      created_at = datetime.strftime(created_datetime, TARGET_DF)
      values = {"id" : str(item["id"]),
                "user_id": str(user_id),
                "created_at": str(created_at),
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type",'')),
                "caption": item.get("caption", '').replace("'",'"'),
                "url": str(item.get("permalink", '')),
                "image": str(item.get("media_url", '')),
                "is_story": 1 if is_story else 0}
      min_date = created_at
      command = utils.from_config('queries.insert_media').format(**values)
      if utils.has_trace_enabled():
          logging.debug("insert media command: %s" % command)
      cursor.execute(command)
  conn.commit()
  cursor.close()
  return min_date

  
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


def process_user_media(conn, user_id, access_token, date_from = None, date_to = None):
    try:
        logging.info("##############################################")
        logging.info("Getting user info for %s" % user_id)      
        url = make_user_url(user_id, access_token)
        response = utils.request_data(url, access_token)
        if response:
            parse_and_insert_info(conn, user_id, response)
            
        logging.info("##############################################")
        logging.info("Getting user media for %s" % user_id)      
        paginate = True
        url = make_media_url(user_id, access_token, date_from, date_to)
        while paginate:
          response = utils.request_data(url, access_token)
          if response and response.get('data'):
            data = response.get('data')
            next_url = response.get('paging').get('next')
            logging.debug("pagination next_url=%s"%next_url)
            min_date = parse_and_insert_media(conn, user_id, data)
            logging.debug("pagination min_date=%s"%min_date)
            if min_date < date_from or next_url == None:
              logging.debug("pagination stopped: min_date=%s"%min_date)
              paginate = False
            url = next_url
          else:
            paginate = False
    except:
        logging.exception("Error while parsing or inserting user or media")

  
def main(args):  
  conf_file = "conf/get_user_media.yaml"
  utils.init(conf_file, True)
  exec_start_time = datetime.now()
  try:
    date_from, date_to = utils.get_start_end_str(args)
    conn = utils.get_conn('ig')
    users = get_users(conn)
    for item in users:
      user_id = item[0]
      access_token = item[1]
      process_user_media(conn, user_id, access_token, date_from, date_to)
    conn.close()
  except:
    logging.exception('Error executing script')
  finally:
    logging.info('Total time: %s' % (datetime.now() - exec_start_time))

if __name__ == '__main__':
     main(sys.argv[1:])

     
