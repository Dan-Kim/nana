import requests

BASE_URL = 'https://cafcp.org/'
MOBILE_BASE_URL = 'https://m.cafcp.org/nocache'

class Cafcp_Request_Wrapper:

  def get_stations(self):
    try:
      endpoint = '{0}/soss2-json-status'.format(MOBILE_BASE_URL)
      r = requests.get(endpoint)
      r.raise_for_status()
      return r.json()
    except requests.exceptions.HTTPError as err:
      return err

  def get_station_message(self, station):
    try:
      endpoint = '{0}/soss2-station-message-output'.format(MOBILE_BASE_URL)
      r = requests.get(endpoint)
      r.raise_for_status()
      return r.json()
    except requests.exceptions.HTTPError as err:
      return err


cafcp_request_wrapper = Cafcp_Request_Wrapper()
