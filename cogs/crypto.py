from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.coinbase_service import coinbase_request_wrapper

CRYPTOCURRENCIES_CHANNELS_MAP = {
  'BTC': [896947895159357470, 902751907364364299],
  'ETH': [896951835028488243, 902751921243308062],
  'LTC': [896951846403448842, 902751934648287333],
  'DOGE': [896951856062930955, 902751945452818592],
  'SOL': [896951865302978620, 902751954403479592],
  'MATIC': [896951875994271754, 902751964453032046],
  'SHIB': [896951892444344330, 902751973311381554],
  'WLUNA': [896952320095576095, 902755844347805767],
  'ADA': [903129388713914388],
  'YFI': [922353295442460763]
}


class Crypto(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.fetch_and_update_crypto_prices, trigger='cron', args=[], max_instances=1, minute='0,5,10,15,20,25,30,35,40,45,50,55')
    self.sched.start()

  async def fetch_and_update_crypto_prices(self):
    for currency, channel_ids in CRYPTOCURRENCIES_CHANNELS_MAP.items():
      response = coinbase_request_wrapper.get_price(currency)
      try:
        amount = response['data']['amount']
        channel_name = '{0}: ${1}'.format(currency, amount)
      except KeyError:
        channel_name = '{0}: FAILED REQUEST'.format(currency)

      for channel_id in channel_ids:
        channel = self.bot.get_channel(channel_id)
        await channel.edit(name=channel_name)
