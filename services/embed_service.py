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
