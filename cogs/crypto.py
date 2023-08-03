from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.embed_service import make_crypto_prices_embed
from services.coinbase_service import coinbase_request_wrapper

PRICE_EMBED_CHANNEL_MESSAGE_DICT = {
  963636436588957696: 963636479706402826, # Vermicelli
  963647470708072558: 963647499216764978, # Mooncrew
  1136431040873893939: 1136431288220393502 # In Z Out
}

CRYPTOCURRENCY_SYMBOLS = [
  ('BTC', 'Bitcoin', '<:btc:963631873404338216>'),
  ('ETH', 'Ethereum', '<:eth:963631874981388328>'),
  ('LTC', 'Litecoin', '<:ltc:963631873437872178>'),
  ('DOGE', 'Dogecoin', '<:doge:963641546765393980>'),
  ('SOL', 'Solana', '<:sol:963631874578718790>'),
  ('MATIC', 'Polygon', '<:matic:963631873328820294>'),
  ('SHIB', 'SHIBA INU', '<:shib:963631874687782922>'),
  #('WLUNA', 'Wrapped Luna', '<:wluna:963631873752444938>'),
  ('ADA', 'Cardano', '<:ada:963631871802114058>'),
  ('YFI', 'yearn.finance', '<:yfi:963631875027529758>'),
  ('AVAX', 'Avalanche', '<:avax:963631871370096661>'),
  ('DOT', 'Polkadot', '<:dot:963631874255753306>'),
  ('RNDR', 'Render Token', '<:rndr:963631870380240966>')
]


class Crypto(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.fetch_and_update_crypto_prices, trigger='cron', args=[], max_instances=1,
                       minute='0,5,10,15,20,25,30,35,40,45,50,55', second='20')
    self.sched.start()

  async def fetch_and_update_crypto_prices(self):
    for channel_id, message_id in PRICE_EMBED_CHANNEL_MESSAGE_DICT.items():
      channel = self.bot.get_channel(channel_id)
      price_message = await channel.fetch_message(message_id)
      await price_message.edit(content='', embed=make_crypto_prices_embed(CRYPTOCURRENCY_SYMBOLS))

  async def price_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing cryptocurrency symbol to search for.')
    return True

  @commands.command(
    description='Look up current spot price of a cryptocurrency on Coinbase.',
    usage='price [CURRENCY SYMBOL]',
    checks=[price_check]
  )
  async def price(self, ctx, *args):
    currency = args[0].upper()
    response = coinbase_request_wrapper.get_price(currency)
    try:
      await ctx.send('{0}: ${1}'.format(currency, response['data']['amount']))
    except TypeError:
      await ctx.send('{0} is not a valid cryptocurrency symbol.'.format(currency))

  @commands.command(
    description='Look up current spot prices for select cryptocurrencies on Coinbase.',
    usage='priceembed'
  )
  async def priceembed(self, ctx, *args):
    await ctx.send(embed=make_crypto_prices_embed(CRYPTOCURRENCY_SYMBOLS))
