from discord.ext import commands

from services.apex_service import get_random_legend
from services.embed_service import make_legend_embed


class Apex(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description='Get random Apex Legends',
    usage='randomlegend',
    aliases=['rl']
  )
  async def randomlegend(self, ctx):
    await ctx.send(
      embed=make_legend_embed(get_random_legend())
    )
