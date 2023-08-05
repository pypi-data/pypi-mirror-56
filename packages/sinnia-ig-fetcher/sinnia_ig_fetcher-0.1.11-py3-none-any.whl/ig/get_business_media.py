import sys, os, requests, copy
import pymysql
import re
import string
from pkg_resources      import resource_string
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAl

class BusinessMediaFetcher:

  SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
  TARGET_DF = "%Y-%m-%d %H:%M:%S"

  def init(self, conf_file, dates_arr):
    exec_start_time = datetime.now()
    try:
      self.utils = InstagramUtils()
      self.utils.init(conf_file, True)
      self.logger = self.utils.get_logger()
      print('BusinessMediaFetcher got logger')
      print(self.logger)
      date_from, date_to = self.utils.get_start_end_str(dates_arr)
      conn = self.utils.get_conn('ig')
      users = self.get_users(conn)
      for item in users:
        user_id = item[0]
        access_token = item[1]
        self.process_business_media(conn, user_id, access_token, date_from, date_to)
      conn.close()
    except:
      self.logger.exception('Error fetching BusinessMedia')
    finally:
      self.logger.info('Total time: %s' % (datetime.now() - exec_start_time))

  
  def make_url(self, type, user_id, access_token, date_from, date_to):
    host = self.utils.from_config('graph_api.host')
    path = self.utils.from_config('graph_api.request_%s_path'%type).format(**locals())
    historic = ''
    if (date_from != None and date_to != None): 
      historic = self.utils.from_config('graph_api.historic_suffix').format(**locals())
    return '%s%s%s'%(host,path,historic)


  def get_users(self, conn):
    users = list()
    print('InstagramUtils get_users logger')
    print(self.logger)
    try:
      query = self.utils.from_config("queries.get_users")
      cursor = conn.cursor(pymysql.cursors.SSCursor)
      cursor.execute(query)
      while (1):
        row = cursor.fetchone()
        if not row:
          break
        user_id = row[0].decode('UTF-8')
        access_token = row[1].decode('UTF-8')
        users.append((user_id, access_token))
        self.logger.debug("Adding user_id %s"%(user_id))
        cursor.close()
        self.logger.debug("Added %s users "%(len(users)))
    except:
      self.logger.exception("Error while getting users")
    return users


  def parse_and_insert(self, conn, user_id, data, is_story=False):
    if len(data) == 0:
      return
    user_values = {"id": user_id, "username": data[0]["username"]}
    command = self.utils.from_config('queries.insert_empty_user').format(**user_values)
    cursor = conn.cursor() 
    self.logger.debug("insert user command: %s" % command)
    cursor.execute(command)
    conn.commit()
    cursor.close()
    
    cursor = conn.cursor()
    for item in data:
      created_datetime = datetime.strptime(item["timestamp"][:19], self.SOURCE_DF)
      created_at = datetime.strftime(created_datetime, self.TARGET_DF)
      values = {"id" : str(item["id"]),
                "user_id": str(user_id),
                "created_at": str(created_at),
                "fetched_at": str(datetime.utcnow()),
                "type": str(item.get("media_type",'')),
                "caption": item.get("caption", '').replace("'",'"'),
                "url": str(item.get("permalink", '')),
                "likes_count": item.get("like_count", 0),
                "comments_count": item.get("comments_count", 0),
                "image": str(item.get("media_url", '')),
                "is_story": 1 if is_story else 0}
      min_date = created_at
      command = self.utils.from_config('queries.insert_media').format(**values)
      if self.utils.has_trace_enabled():
          self.logger.debug("insert command: %s" % command)
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
#   self.logger.debug('alert url: %s' % url)
#   self.logger.debug('alert body: %s...' % body[:250])
#   r = requests.post(url, body)

  def process_business_media(self, conn, user_id, access_token, date_from = None, date_to = None):
    try:
        self.logger.info("##############################################")
        self.logger.info("Getting media for %s" % user_id)      
        paginate = True
        url = self.make_url('media',user_id,access_token,date_from,date_to)
        while paginate:
          response = self.utils.request_data(url, access_token)
          if response and response.get('data'):
            data = response.get('data')
            next_url = response.get('paging').get('next')
            self.logger.debug("pagination next_url=%s"%next_url)
            min_date = self.parse_and_insert(conn, user_id, data)
            self.logger.debug("pagination min_date=%s"%min_date)
            if min_date < date_from or next_url == None:
              self.logger.debug("pagination stopped: min_date=%s"%min_date)
              paginate = False
            url = next_url
          else:
            paginate = False
                  
        self.logger.info("##############################################")
        self.logger.info("Getting stories for %s" % user_id)
        url = self.make_url('stories',user_id,access_token,date_from,date_to)
        response = self.utils.request_data(url, access_token)
        if response and response.get('data'):
          self.parse_and_insert(conn, user_id, response.get('data'), True)
    except:
        self.logger.exception("Error while parsing or inserting stories")
        
  
def main(args):
  #conf_file = resource_string(__name__, 'conf/get_business_media.yaml')
  conf_file = "conf/get_business_media.yaml"
  fetcher = BusinessMediaFetcher()
  fetcher.init(conf_file, args)

if __name__ == '__main__':
     main(sys.argv[1:])

     
