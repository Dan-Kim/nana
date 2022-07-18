import discord
from discord.ext import commands
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import xml.etree.ElementTree as ET

from constants import MYANIMELIST_RSS_FEED_CHANNEL_ID

from services.db_service import select_mal_users
from services.embed_service import make_rss_feed_update_embed
from services.myanimelist_service import get_rss_feeds_for_user


class MyAnimeList(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.poll_rss_feeds, trigger='cron', args=[], max_instances=1, minute='0,5,10,15,20,25,'
                                                                                                  '30,35,40,45,50,55')
    self.sched.start()

  async def poll_rss_feeds(self):
    channel = discord.Client.get_channel(self=self.bot, id=MYANIMELIST_RSS_FEED_CHANNEL_ID)
    for row in select_mal_users():
      user = row[0]
      for media_type, response_text in get_rss_feeds_for_user(user).items():
        xml = ET.ElementTree(ET.fromstring(response_text))
        for item in xml.findall('./channel/item'):
          media_title, link, description, pub_date = item[0], item[1], item[3], item[4]
          pub_timestamp = datetime.strptime(pub_date.text, '%a, %d %b %Y %H:%M:%S %z').timestamp()
          if pub_timestamp > (datetime.now() - timedelta(minutes=10)).timestamp():
            await channel.send(embed=make_rss_feed_update_embed(media_title=media_title.text, link=link.text,
                                                                description=description.text, pub_date=pub_date.text,
                                                                media_type=media_type, user=user))
          else:
            break
