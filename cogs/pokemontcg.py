from discord.ext import commands
from datetime import datetime, timedelta
import pytz
from itertools import cycle
from apscheduler.schedulers.asyncio import AsyncIOScheduler

UTC = pytz.timezone('UTC')

from services.embed_service import make_pokemon_card_embed
from services.pokemontcg_service import get_cards_by_name


class PokemonTCG(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.remove_card_iter, trigger='cron', args=[], max_instances=1, second='5')
    self.sched.start()
    self.card_iters = {}

  async def remove_card_iter(self):
    for key in list(self.card_iters):
      _, timestamp = self.card_iters[key]
      if datetime.now().timestamp() > timestamp:
        del self.card_iters[key]

  @commands.command(
    description='Find all cards by name',
    usage='searchcard [NAME]',
    aliases=['sc']
  )
  async def searchcard(self, ctx, *args):
    query = ' '.join(args)
    cards = get_cards_by_name(query)
    forward = cycle(cards)
    try:
      message = await ctx.send(embed=make_pokemon_card_embed(next(forward)))
    except StopIteration:
      await ctx.send('No cards with the name `{0}`.'.format(query))
      return
    key = str(ctx.author.id) + str(message.id)
    self.card_iters[key] = (forward, (datetime.now() + timedelta(seconds=30)).timestamp())

  async def handle_reaction(self, payload):
    key = str(payload.user_id) + str(payload.message_id)
    if key in self.card_iters:
      channel = self.bot.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      await message.edit(embed=make_pokemon_card_embed(next(self.card_iters[key][0])))

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    await self.handle_reaction(payload)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    await self.handle_reaction(payload)
