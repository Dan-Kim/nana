from typing import List

from datetime import datetime
import discord
import random

from constants import PREFIX
from models.remind import Remind
from services.coinbase_service import coinbase_request_wrapper
from services.time_service import get_time_from_epoch

COLORS = [0xfd5e53, 0xeaebff, 0xe0fefe, 0xd3eeff, 0xffd6f3]


#############################
# MISC PLUGIN EMBED METHODS #
#############################

def make_help_embed(commands):
  embed = discord.Embed(title='Help',
                        description='Available commands. Prefix: `{0}`. All times are in Pacific Time.'.format(PREFIX),
                        color=random.choice(COLORS))
  for key, value in commands.items():
    embed.add_field(name=key, value=value, inline=False)
  return embed


def make_harpsichord_embed(doc):
  embed = discord.Embed(title='Harpsichord Room Sensor Data', description='チェンバロ室センサーデータ', color=random.choice(COLORS))
  embed.add_field(name='Time', value='<t:{0}:F>'.format(doc['timestamp']))
  temp_c = round(doc['temperature'], 2)
  temp_f = round(doc['temperature'] * 9 / 5 + 32, 2)
  embed.add_field(name='Temperature', value='{0} °C\n{1} °F'.format(temp_c, temp_f))
  embed.add_field(name='Humidity', value='{0}%'.format(round(doc['humidity'], 2)))
  return embed


###############################
# REMIND PLUGIN EMBED METHODS #
###############################

def make_remind_embed(reminds: List[Remind]):
  embed = discord.Embed(title='Your reminds', description='Enter 0 to delete a remind', color=random.choice(COLORS))
  for i, remind in enumerate(reminds):
    embed.add_field(name='Remind {0} at {1}'.format(i + 1, get_time_from_epoch(remind.requested_time)),
                    value=remind.message, inline=False)
  return embed


####################################
# MINECRAFT PLUGIN EMBED CONSTANTS #
####################################

THUMBNAIL_URLS = [
  'https://i.redd.it/la9d3c49c9s51.jpg',
  'https://design-kom.com/design/wp-content/uploads/2018/01/l102.3.jpg',
  'https://staticdelivery.nexusmods.com/mods/2531/images/thumbnails/2721/2721-1583430189-1782774948.png',
  'https://www.minecraftskins.com/uploads/preview-skins/2020/10/09/peepo-elegant-15461918.png?v288',
  'https://images-na.ssl-images-amazon.com/images/I/512dVKB22QL._AC_UL600_SR600,600_.png'
]


##################################
# MINECRAFT PLUGIN EMBED METHODS #
##################################

def make_minecraft_embed(allocation_json, utilization_json):
  embed = discord.Embed(title='Memeteam Kensetsu Info', description='ミームチーム建設情報の一覧', color=random.choice(COLORS))
  embed.set_thumbnail(url=random.choice(THUMBNAIL_URLS))
  try:
    allocation = allocation_json['attributes']['relationships']['allocations']['data'][0]['attributes']
    embed.add_field(name='IP', value='{0}:{1}'.format(allocation['ip'], allocation['port']), inline=False)
  except (KeyError, IndexError):
    embed.add_field(name='IP', value='No IP allocated for this server.')

  try:
    utilization = utilization_json['attributes']
  except KeyError:
    embed.add_field(name='Utilization Info',
                    value='Unable to fetch server state, memory usage, disk usage, CPU usage, and online players.')
    return embed

  try:
    embed.add_field(name='Server State', value=utilization['state'].capitalize())
  except KeyError:
    embed.add_field(name='Server State', value='Unable to fetch server state.')

  try:
    embed.add_field(name='Memory Usage',
                    value='{0}/{1} MB'.format(utilization['memory']['current'], utilization['memory']['limit']))
  except KeyError:
    embed.add_field(name='Memory Usage', value='Unable to fetch memory usage.')

  try:
    embed.add_field(name='Disk Usage',
                    value='{0}/{1} MB'.format(utilization['disk']['current'], utilization['disk']['limit']))
  except KeyError:
    embed.add_field(name='Disk Usage', value='Unable to fetch disk usage.')

  try:
    cpu_cores_usages = '\n'.join(
      ['**Core {0}**: {1}%'.format(i + 1, v) for i, v in enumerate(utilization['cpu']['cores'])])
    cpu_total_usage = '**Total**: {0}%'.format(utilization['cpu']['current'])
    embed.add_field(name='CPU Usage', value='{0}\n{1}'.format(cpu_cores_usages, cpu_total_usage), inline=False)
  except:
    embed.add_field(name='CPU Usage', value='Unable to fetch CPU usage.', inline=False)

  try:
    num_players = len(utilization['query']['players'])
    current_online_players_name = 'Current Online Players {0}/{1}'.format(num_players,
                                                                          utilization['query']['maxplayers'])
    if num_players == 0:
      current_online_players_value = 'No players online'
    else:
      current_online_players_value = ', '.join([player['name'] for player in utilization['query']['players']])
    embed.add_field(name=current_online_players_name, value=current_online_players_value, inline=False)
  except KeyError:
    embed.add_field(name='Current Online Players (?/?)', value='Unable to fetch current online players.', inline=False)
  return embed


#############################
# APEX PLUGIN EMBED METHODS #
#############################

def make_legend_embed(legend_arr):
  embed = discord.Embed(title=legend_arr[0], description=legend_arr[1], color=random.choice(COLORS))
  embed.set_image(url=legend_arr[2])
  return embed


###############################
# CRYPTO PLUGIN EMBED METHODS #
###############################

def make_crypto_prices_embed(cryptocurrency_symbols):
  embed = discord.Embed(title='Cryptocurrency Spot Prices',
                        description='Updated as of <t:{0}:f>'.format(int(datetime.now().timestamp())),
                        color=random.choice(COLORS))
  embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1484586799921909764/A9yYenz3.png')
  for (symbol, name, emote) in cryptocurrency_symbols:
    price = coinbase_request_wrapper.get_price(symbol)
    embed.add_field(name='{0} {1} ({2})'.format(emote, name, symbol), value='${0}'.format(price['data']['amount']),
                    inline=False)
  return embed


###################################
# POKEMONTCG PLUGIN EMBED METHODS #
###################################

def make_pokemon_card_embed(card):
  embed = discord.Embed(title=card.name, description='ID: {0}'.format(card.id), color=random.choice(COLORS))
  embed.set_image(url=card.images.large)
  embed.add_field(name='Market Prices',
                  value='[CardMarket]({0})\n[TCGPlayer]({1})'.format(card.cardmarket.url, card.tcgplayer.url))
  return embed


####################################
# MYANIMELIST PLUGIN EMBED METHODS #
####################################

def make_rss_feed_update_embed(media_title, link, description, pub_date, media_type, user):
  embed = discord.Embed(title='{0}\'s {1} from MyAnimeList.net'.format(user, media_type.capitalize()),
                        description='Updated {0}'.format(pub_date), color=random.choice(COLORS))
  embed.add_field(name=media_title, value='{0}\n{1}'.format(description, link))
  return embed
