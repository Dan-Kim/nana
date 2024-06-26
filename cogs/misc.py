import discord
from discord.ext import commands
import os
import time
import re

from constants import ADMIN_DISCORD_ID, COMMAND_USAGE_CHANNEL_ID, PREFIX

from services.embed_service import make_help_embed
from services.jisho_service import search_jisho
from services.time_service import get_current_japan_time


class Miscellaneous(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command('help')
    self.command_usage_dict = {}
    self.command_description_dict = {}

  def init_command_description_dict(self):
    if not self.command_description_dict:
      for command in self.bot.commands:
        self.command_description_dict[command.name] = command.description

  def init_command_usage_dict(self):
    if not self.command_usage_dict:
      for command in self.bot.commands:
        if command.cog.qualified_name not in self.command_usage_dict:
          self.command_usage_dict[command.cog.qualified_name] = command.usage
        else:
          self.command_usage_dict[command.cog.qualified_name] += '\n{0}'.format(command.usage)
      for cog_name, usage in self.command_usage_dict.items():
        self.command_usage_dict[cog_name] = '```ini\n{0}\n```'.format(usage)

  async def jisho_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing input to search Jisho.')
    return True

  @commands.command(
    description='Search jisho for a translation. Input can be Japanese or English.',
    usage='jisho [SEARCH TERM]',
    checks=[jisho_check]
  )
  async def jisho(self, ctx, *args):
    query = ' '.join(args)
    output = search_jisho(query)
    await ctx.send(output)

  async def admin_check(ctx):
    if ctx.author.id != ADMIN_DISCORD_ID:
      raise commands.CommandError(message='You are not allowed to access this command.')
    return True

  async def set_playing_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing input to set as playing.')
    return True

  @commands.command(
    description='Set the playing status of the bot.',
    usage='setplaying [STRING]',
    checks=[admin_check, set_playing_check]
  )
  async def setplaying(self, ctx, *args):
    s = ' '.join(args)
    await discord.Client.change_presence(self=self.bot, activity=discord.Game(name=s))

  @commands.command(
    description='Get the current time in Japan.',
    usage='jst'
  )
  async def jst(self, ctx):
    await ctx.send(':japan: {0}'.format(get_current_japan_time()))

  @commands.command(
    description='Pain Peko.',
    usage='painpeko'
  )
  async def painpeko(self, ctx):
    folder = os.path.dirname(os.path.realpath('__file__'))
    await ctx.send(file=discord.File(os.path.join(folder, '../nana-db/assets/painpeko.png')))

  @commands.command(
    description='mogu mogu okayun!',
    usage='mogumogu'
  )
  async def mogumogu(self, ctx):
    folder = os.path.dirname(os.path.realpath('__file__'))
    await ctx.send(file=discord.File(os.path.join(folder, '../nana-db/assets/okayun.gif')))
    time.sleep(3)

  @commands.Cog.listener()
  async def on_message(self, message):
    if re.search(".*mogu.*mogu.*", message.content, re.IGNORECASE):
      channel = self.bot.get_channel(message.channel.id)
      await channel.send('Okayu!')

  @commands.command(
    description='Get the help message with proper usage instructions.',
    usage='help [optional COMMAND]'
  )
  async def help(self, ctx, *args):
    if args:
      self.init_command_description_dict()
      query = ' '.join(args)
      try:
        description = self.command_description_dict[query]
        await ctx.send(description)
      except KeyError:
        await ctx.send('There is no command called {0}.'.format(query))
    else:
      self.init_command_usage_dict()
      await ctx.send(embed=make_help_embed(self.command_usage_dict))

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.content.startswith(PREFIX):
      usage_channel = self.bot.get_channel(COMMAND_USAGE_CHANNEL_ID)
      if len(message.content) >= 1900:
        await usage_channel.send('*Part 1*\n**{0}**: {1}'.format(message.author, message.content[0:1000]))
        await usage_channel.send('*Part 2*\n**{0}**: {1}'.format(message.author, message.content[1000:]))
      else:
        await usage_channel.send('**{0}**: {1}'.format(message.author, message.content))
