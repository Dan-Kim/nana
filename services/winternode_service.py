import requests
from constants import WINTERNODE_SERVER_UUID
from credentials import WINTERNODE_API_KEY

ALLOCATION_URL = 'https://gcp.winternode.com/api/client/servers/{0}?include=allocations'.format(WINTERNODE_SERVER_UUID)
RESOURCES_URL = 'https://gcp.winternode.com/api/client/servers/{0}/resources'.format(WINTERNODE_SERVER_UUID)


class WinterNode_Request_Wrapper:
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.wisp.v1+json',
    'Authorization': 'Bearer {0}'.format(WINTERNODE_API_KEY)
  }

  def get_allocation_data(self):
    try:
      r = requests.get(ALLOCATION_URL, headers=self.headers)
      r.raise_for_status()
      return r.json()
    except requests.exceptions.HTTPError as err:
      return err

  def get_resources_data(self):
    try:
      r = requests.get(RESOURCES_URL, headers=self.headers)
      r.raise_for_status()
      return r.json()
    except requests.exceptions.HTTPError as err:
      return err


winterNode_Request_Wrapper = WinterNode_Request_Wrapper()
