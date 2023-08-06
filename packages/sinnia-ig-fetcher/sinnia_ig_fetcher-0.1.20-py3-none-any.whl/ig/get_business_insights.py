import sys, os, logging, requests, copy
import pymysql
import re
import string
from datetime           import time, timedelta, datetime, tzinfo, date
from ig.instagram_utils import InstagramUtils
#from alerts_pb2 import InternalAlert

#https://developers.facebook.com/docs/instagram-api/reference/user/insights

utils = InstagramUtils()
errors = list()

SOURCE_DF = "%Y-%m-%dT%H:%M:%S"
TARGET_DF = "%Y-%m-%d %H:%M:%S"
DF = "%Y-%m-%d"

logging.basicConfig(filename='logs/get_business_insights.log',level=logging.DEBUG)
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)


def get_audience_table(name):
    return {
        'audience_gender_age': 'UserInsightsAudienceGenderAge',
        'audience_locale':     'UserInsightsAudienceLocales',
        'audience_city':       'UserInsightsAudienceCities',
        'audience_country':    'UserInsightsAudienceCountries'
    }.get(name,'')


def request_data(type, user_id, access_token, period,
                 date_from = None, date_to = None):
  host = utils.from_config('graph_api.host')
  daily = '_daily' if period == 'day' else ''
  path_name = 'graph_api.request_%s%s_path' % (type, daily)
  path = utils.from_config(path_name).format(**locals())
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
    users = list()
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


def parse_and_insert(conn, user_id, metrics):  
  cursor = conn.cursor()  
  for item in metrics:
      metric_name = str(item["name"])
      common_fields = {"user_id": user_id,
                       "period": str(item["period"]),
                       "fetched_time": str(datetime.utcnow())}
      for values in item["values"]:          
          end_datetime = datetime.strptime(values["end_time"][:19],
                                           SOURCE_DF)
          end_time = datetime.strftime(end_datetime, TARGET_DF)
          fields = {"metric_name": metric_name,
                    "metric_value": values["value"],
                    "end_time": str(end_time)}
          fields.update(common_fields)
          logging.debug("insert with fields: %s" % str(fields))
          command = utils.from_config('queries.insert_basic').format(**fields)
          if utils.has_trace_enabled():
              logging.debug("insert command: %s" % command)
          cursor.execute(command)
  conn.commit()
  cursor.close()



def parse_and_insert_audiences(conn, user_id, metrics):  
  cursor = conn.cursor()  
  for metric in metrics:
      metric_name = str(metric["name"])
      common_fields = {"user_id": user_id,
                       "period": metric["period"],
                       "fetched_time": str(datetime.utcnow())}
      if metric_name == "audience_gender_age":
          values = metric["values"][0] # only one value because it's Lifetime
          end_datetime = datetime.strptime(values["end_time"][:19],
                                           SOURCE_DF)
          end_time = datetime.strftime(end_datetime, TARGET_DF)
          pairs = values["value"]
          if len(pairs.items()) == 0:
              logging.debug("no values for %s metric: %s" % (str(end_time), metric_name))
          for key, value in pairs.items():
              gender = key.split('.')[0]
              age = key.split('.')[1]
              fields = {"gender": gender,
                        "age": age,
                        "metric_value": value,
                        "end_time": str(end_time)}
              fields.update(common_fields)
              logging.debug("insert with fields: %s" % str(fields))
              command = utils.from_config('queries.insert_audience_gender_age').format(**fields)
              if utils.has_trace_enabled():
                  logging.debug("insert command: %s" % command)
              cursor.execute(command)
          conn.commit()
      else:
          values = metric["values"][0] # only one value because it's Lifetime
          end_datetime = datetime.strptime(values["end_time"][:19],
                                           SOURCE_DF)
          end_time = datetime.strftime(end_datetime, TARGET_DF)
          pairs = values["value"]
          if len(pairs.items()) == 0:
              logging.debug("no values for %s metric: %s" % (str(end_time), metric_name))
          for key, value in pairs.items():
              fields = {"table_name": get_audience_table(metric_name),
                        "metric_name": key,
                        "metric_value": value,
                        "end_time": str(end_time)}
              fields.update(common_fields)
              logging.debug("insert with fields: %s" % str(fields))
              command = utils.from_config('queries.insert_audience_location').format(**fields)
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


def process_business_insights(conn, user_id, access_token, date_from = None, date_to = None):
    try:
        ## Basic metrics: unavailable for Lifetime; iterate in 30-day intervals
        periods = ['day','week','days_28']
        partial_to   = date_to
        partial_from = partial_to + timedelta(days=-30)
        while partial_to >= date_from:
            logging.info('part_from %s part_to %s'%(partial_from,partial_to))
            for period in periods: 
              logging.info("##############################################")
              logging.info('Getting basic insights for %s from %s to %s (%s)'%
                           (user_id, partial_from, partial_to, period))
              response = request_data('basic', user_id, access_token, period,
                                      datetime.strftime(partial_from, DF),
                                      datetime.strftime(partial_to, DF))
              if response:
                  parse_and_insert(conn, user_id, response.get('data'))
            partial_to   = partial_from
            partial_from = partial_to + timedelta(days=-30)
            
        ## Audience metrics: only available for Lifetime; without since/until
        period = 'lifetime'
        logging.info("##############################################")
        logging.info('Getting audience insights for %s from %s to %s (%s)' %
                     (user_id, date_from, date_to, period))
        response = request_data('audiences', user_id, access_token, period) 
        if response:
            parse_and_insert_audiences(conn, user_id, response.get('data'))
    except:
        logging.exception("Error getting, parsing or inserting metrics")

  
def main(args):  
  conf_file = "conf/get_business_insights.yaml"
  utils.init(conf_file, True)
  exec_start_time = datetime.now()
  try:
    date_from, date_to = utils.get_start_end_dates(args)
    conn = utils.get_conn('ig')
    users = get_users(conn)
    for item in users:
      user_id = item[0]
      access_token = item[1]
      process_business_insights(conn, user_id, access_token, date_from, date_to)
    conn.close()
  except:
    logging.exception('Error executing script')
  finally:
    logging.info('Total time: %s' % (datetime.now() - exec_start_time))

if __name__ == '__main__':
     main(sys.argv[1:])
