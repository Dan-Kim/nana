import requests

from credentials import ENCODED_COINBASE_API_KEY

BASE_URL = 'https://api.coinbase.com/v2/prices/'
URL_SUFFIX = '-USD/spot'


class Coinbase_Request_Wrapper:
  headers = {
    'Authorization': 'Bearer {0}'.format(ENCODED_COINBASE_API_KEY)
  }

  def get_price(self, currency):
    try:
      endpoint = ''.join([BASE_URL, currency, URL_SUFFIX])
      r = requests.get(endpoint, headers=self.headers)
      r.raise_for_status()
      return r.json()
    except requests.exceptions.HTTPError as err:
      return err


coinbase_request_wrapper = Coinbase_Request_Wrapper()
