import discord
from discord.ext.commands import Bot

from constants import PREFIX
from credentials import DISCORD_TOKEN

from cogs.apex import Apex
from cogs.banner import Banner
from cogs.crypto import Crypto
from cogs.misc import Miscellaneous
from cogs.myanimelist import MyAnimeList

intents = discord.Intents.all()

cogs = [Apex, Banner, Crypto, Miscellaneous, MyAnimeList]


class Nana(Bot):
  def __init__(self):
    super().__init__(command_prefix=PREFIX, description='Nana.', intents=intents)

  async def on_ready(self):
    await self.load_cogs(cogs)
    print('Logged in as {0.user.name}'.format(self))

  async def load_cogs(self, cogs):
    for cog in cogs:
      try:
        await self.add_cog(cog(self))
        print('{0} has been loaded.'.format(cog))
      except discord.ClientException as CE:
        print('Client Exception: {0}'.format(CE))
      except ImportError as IE:
        print('Import Error: {0}'.format(IE))

if __name__ == '__main__':
  bot = Nana()


  @Bot.listen(name='on_command_error', self=bot)
  async def on_command_error(ctx, error):
    await ctx.send('{0}\nUsage: `{1}{2}`'.format(error, PREFIX, ctx.command.usage)[:2000])


  bot.run(DISCORD_TOKEN)
