import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

from constants import MEMETEAM_DISCORD_SERVER_ID, BANNER_COMMAND_VALID_DISCORD_SERVER_IDS

from serializers.banner_serializer import get_banner, get_random_banner

from services.db_service import increment_banner_count

PERMITTED_BANNER_FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


class Banner(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.update_memeteam_banner, trigger='cron', args=[], max_instances=1,
                       hour='0,4,8,12,16,20', timezone='US/Pacific')
    self.sched.start()

  async def update_memeteam_banner(self):
    guild = self.bot.get_guild(MEMETEAM_DISCORD_SERVER_ID)
    banner_row = get_random_banner()
    banner_file_path = self.get_banner_file_path(str(banner_row['discord_id']))
    with open(banner_file_path, 'rb') as f:
      banner = f.read()
      await guild.edit(banner=banner)
      increment_banner_count(banner_row['discord_id'])

  async def guild_check(ctx):
    guild_id = ctx.message.guild.id
    if guild_id not in BANNER_COMMAND_VALID_DISCORD_SERVER_IDS:
      raise commands.CommandError(message='This command is not available in this server.')
    return True

  async def banner_permission_check(ctx):
    banner_row = get_banner(discord_id=ctx.message.author.id)
    if not banner_row:
      raise commands.CommandError(message='You do not have permission to submit a banner.')
    return True

  @commands.command(
    description='Display your banner submission.',
    usage='banner',
    checks=[guild_check]
  )
  async def banner(self, ctx):
    if not self.has_banner(str(ctx.message.author.id)):
      await ctx.send('No banner submission found.')
    else:
      banner_row = get_banner(ctx.message.author.id)[0]
      await ctx.send('<@!{0}>\'s submission. Randomly selected {1} times.'.format(banner_row['discord_id'],
                                                                                  banner_row['times_picked']))
      await ctx.send(file=discord.File(self.get_banner_file_path(str(banner_row['discord_id']))))

  @commands.command(
    description='Submit a banner. It may replace an existing banner.',
    usage='submitbanner',
    checks=[guild_check, banner_permission_check]
  )
  async def submitbanner(self, ctx):
    banner_row = get_banner(discord_id=ctx.message.author.id)[0]
    if self.has_banner(str(banner_row['discord_id'])):
      await ctx.send('<@!{0}>\'s submission will be replaced. Please upload a file now. Valid file types: {1}'.format(
        banner_row['discord_id'], ', '.join(PERMITTED_BANNER_FILE_TYPES)))
    else:
      await ctx.send('<@!{0}> currently has no submission. Please upload a file now. Valid file types: {1}'.format(
        banner_row['discord_id'], ', '.join(PERMITTED_BANNER_FILE_TYPES)))

    def banner_submission_check(message):
      return message.author.id == ctx.message.author.id and message.attachments[0].filename.split('.')[
        -1] in PERMITTED_BANNER_FILE_TYPES

    message = await discord.Client.wait_for(self.bot, 'message', timeout=60.0, check=banner_submission_check)
    if self.has_banner(str(banner_row['discord_id'])):
      os.remove(self.get_banner_file_path(str(banner_row['discord_id'])))
    await message.attachments[0].save(
      '{0}.{1}'.format(os.path.join(self.get_banner_folder(), str(banner_row['discord_id'])),
                       message.attachments[0].filename.split('.')[-1]))
    await ctx.send('Successfully saved new banner submission.')

  def has_banner(self, discord_id):
    folder = self.get_banner_folder()
    for file in os.listdir(folder):
      if discord_id in file:
        return True
    return False

  def get_banner_file_path(self, discord_id):
    folder = self.get_banner_folder()
    file = [x for x in os.listdir(folder) if discord_id in x][0]
    return os.path.join(folder, file)

  def get_banner_folder(self):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    folder = os.path.join(file_dir, '../nana-db/assets/banners')
    return folder
