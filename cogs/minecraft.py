from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pprint
from constants import ADMIN_DISCORD_ID, MINECRAFT_SERVER_INFO_CHANNEL_ID, MINECRAFT_SERVER_INFO_EMBED_MSG_ID, \
  MINECRAFT_COMMAND_VALID_DISCORD_SERVER_IDS, MINECRAFT_SERVER_INFO_CATEGORY_ID
from services.embed_service import make_minecraft_embed
from services.time_service import get_current_timestamp
from services.winternode_service import winterNode_Request_Wrapper

pp = pprint.PrettyPrinter(indent=4)


class Minecraft(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.fetch_and_update_server_info, trigger='cron', args=[], max_instances=1, minute='5')
    self.sched.start()

  async def guild_check(ctx):
    guild_id = ctx.message.guild.id
    if guild_id not in MINECRAFT_COMMAND_VALID_DISCORD_SERVER_IDS:
      raise commands.CommandError(message='This command is not available in this server.')
    return True

  async def admin_check(ctx):
    if ctx.author.id != ADMIN_DISCORD_ID:
      raise commands.CommandError(message='You are not allowed to access this command.')
    return True

  @commands.command(
    description='Get Minecraft server info',
    usage='server',
    checks=[guild_check]
  )
  async def server(self, ctx):
    await ctx.send(
      embed=make_minecraft_embed(winterNode_Request_Wrapper.get_allocation_data(),
                                 winterNode_Request_Wrapper.get_resources_data(),
                                 get_current_timestamp()))

  @commands.command(
    description='Pretty print Winternode API calls for debugging purposes',
    usage='pprint',
    checks=[guild_check, admin_check]
  )
  async def pprint(self, ctx):
    print("ALLOCATION")
    pp.pprint(winterNode_Request_Wrapper.get_allocation_data())
    print("RESOURCES")
    pp.pprint(winterNode_Request_Wrapper.get_resources_data())

  async def fetch_and_update_server_info(self):
    resources_json = winterNode_Request_Wrapper.get_resources_data()
    category = self.bot.get_channel(MINECRAFT_SERVER_INFO_CATEGORY_ID)
    try:
      await category.edit(name='CobblersUnited {0}/{1}'.format(len(resources_json['query']['players']),
                                                               resources_json['query']['maxplayers']))
    except KeyError:
      await category.edit(name='CobblersUnited (?/?)')
    channel = self.bot.get_channel(MINECRAFT_SERVER_INFO_CHANNEL_ID)
    server_info_message = await channel.fetch_message(MINECRAFT_SERVER_INFO_EMBED_MSG_ID)
    await server_info_message.edit(content='',
                                   embed=make_minecraft_embed(winterNode_Request_Wrapper.get_allocation_data(),
                                                              resources_json,
                                                              get_current_timestamp()))
