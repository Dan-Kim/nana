from credentials import POKEMONTCG_API_KEY
from pokemontcgsdk import RestClient, Card

RestClient.configure(POKEMONTCG_API_KEY)

def get_cards_by_name(name):
  return Card.where(q='name:{0}'.format(name))
