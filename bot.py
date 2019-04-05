#!/usr/bin/env python3

""" the stock bot """

import json
import logging
import os
import sys
import traceback

import discord
from discord.ext import commands

# setup


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # credit to @EvieePy, this is based on her example
    prefixes = ['sb!', 'stocks', '!!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.member', 'cogs.owner', 'cogs.simple', 'cogs.stock']

logging.basicConfig(level=logging.INFO, format=(
    '%(asctime)s %(levelname)s %(name)s | %(message)s'))

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)

description = '''possibly the most stupid bot to have ever been created'''
bot = commands.Bot(command_prefix='sb!', description=description)

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.exception(
                f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='sb! | the stock bot | @djmango'))

# login
if os.getenv('BOTKEY'):
    bot.run(os.getenv('BOTKEY'))
else:
    with open('keys.json') as f:
        keys = json.load(f)
        bot.run(keys['botKey'])
