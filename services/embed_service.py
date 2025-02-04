from datetime import datetime
import discord
import random

from constants import PREFIX
from services.coinbase_service import coinbase_request_wrapper

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


####################################
# MINECRAFT PLUGIN EMBED CONSTANTS #
####################################

THUMBNAIL_URLS = [
  'https://cdn2.steamgriddb.com/icon_thumb/5cc8dfeade12d0c5cd741edb9ae24d81.png'
]


##################################
# MINECRAFT PLUGIN EMBED METHODS #
##################################

def make_minecraft_embed(allocation_json, resources_json, current_timestamp):
  embed = discord.Embed(title='CobblersUnited', description='Updated <t:{0}:F>'.format(current_timestamp), color=random.choice(COLORS))
  embed.set_thumbnail(url=random.choice(THUMBNAIL_URLS))
  try:
    allocation = allocation_json['attributes']['relationships']['allocations']['data'][0]['attributes']
    embed.add_field(name='IP', value='{0}:{1}'.format(allocation['ip'], allocation['port']), inline=False)
  except (KeyError, IndexError):
    embed.add_field(name='IP', value='No IP allocated for this server.')

  try:
    resources = resources_json['proc']
  except KeyError:
    embed.add_field(name='Resources Info',
                    value='Unable to fetch server state, memory usage, disk usage, CPU usage, and online players.')
    return embed

  try:
    embed.add_field(name='Server State', value='ON' if resources_json['status'] == 1 else 'OFF', inline=False)
  except KeyError:
    embed.add_field(name='Server State', value='Unable to fetch server state.', inline=False)

  try:
    embed.add_field(name='Memory Usage',
                    value='{0}%'.format(round(resources['memory']['total']/resources['memory']['limit']*100), 2),
                    inline=False)
  except KeyError:
    embed.add_field(name='Memory Usage', value='Unable to fetch memory usage.', inline=False)

  try:
    num_players = len(resources_json['query']['players'])
    current_online_players_name = 'Current Online Players {0}/{1}'.format(num_players,
                                                                          resources_json['query']['maxplayers'])
    if num_players == 0:
      current_online_players_value = 'No players online'
    else:
      current_online_players_value = '\n'.join(resources_json['query']['players'])
    embed.add_field(name=current_online_players_name, value=current_online_players_value, inline=False)
  except KeyError:
    embed.add_field(name='Current Online Players (?/?)', value='Unable to fetch current online players.', inline=False)
  return embed


######################################
# MYANIMELIST PLUGIN EMBED CONSTANTS #
######################################

WHITE = 0xffffff
BLUE = 0x0000ff


####################################
# MYANIMELIST PLUGIN EMBED METHODS #
####################################

def make_rss_feed_update_embed(media_type, user, updates):
  embed = discord.Embed(title='{0}\'s {1} Updates from MyAnimeList.net'.format(user, media_type),
                        description='https://myanimelist.net/profile/{0}'.format(user),
                        color=BLUE if 'Anime' in media_type else WHITE)
  for media_title, link, description, pub_timestamp in updates:
    embed.add_field(name=media_title, value='{0}\n{1}\n<t:{2}>'.format(link, description, pub_timestamp), inline=False)
  return embed
