from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.cafcp_service import cafcp_request_wrapper

class Hydrogen(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description='List hydrogen stations.',
    usage='stations'
  )
  async def stations(self, ctx):
    for node, station in cafcp_request_wrapper.get_station_message('15024').items():
      await ctx.send('\n'.join(['**{0}**: {1}'.format(' '.join([s.capitalize() for s in key.split('_')]), value) for key, value in station['node'].items() if value]))
