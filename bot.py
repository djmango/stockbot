#!/usr/bin/env python3

""" stock bot """

import asyncio
import logging
import os
import sched
import time
import traceback
import threading

import discord
from discord.ext import commands
from dotenv import load_dotenv

# setup
s = sched.scheduler(time.time, time.sleep)
if os.getenv('BOTKEY') is None:
    load_dotenv('keys.env')

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.member', 'cogs.owner', 'cogs.simple']

logging.basicConfig(level=logging.INFO, format=(
    '%(asctime)s %(levelname)s %(name)s | %(message)s'))

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)

description = '''kc's stock bot.'''
bot = commands.Bot(command_prefix='$', description=description)

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.exception(f'Failed to load {extension}.')
            traceback.print_exc()

# utility functions
def isValidRecipient(user, guild):

    if user.upper() in guild:
        return True
    else:
        return False

async def yell():
        msg = """Hey there! Happy Thanksgiving! :turkey: We have so much to be thankful for and I want to start by thanking you for being a pat of the $1DollarStockPicks server. We have grown to nearly 1700 members in just 1 year and it’s been an amazing journey.  In appreciation and Thanksgiving celebration, we’re giving any 1st time members a FREE month to check out the entire server. Just subscribe Monthly and use promo code THANKSGIVING. Again, thanks for being a part of our great community and I wish you the very best holiday season. -Doc"""
        # user = discord.utils.find(lambda m: m.name == 'Doc', bot.users)
        # user = discord.utils.find(lambda m: m.name == 'djmango', bot.users)
        # await user.send(msg)
        for user in bot.users:
            try:
                logger.debug('yelling at ' + user.name)
                await user.send(msg)
            except:
                logger.debug('cant yell at ' + user.name)
                pass

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')
    await yell()

# login
bot.run(os.getenv('BOTKEY'))
