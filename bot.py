#!/usr/bin/env python3

""" purple king bot """

import json
import logging
import os
import traceback
import asyncio
import random

import discord
from discord.ext import commands

# setup


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # credit to @EvieePy, this is based on her example
    prefixes = ['!', '!!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.member', 'cogs.simple', 'cogs.ad']

logging.basicConfig(level=logging.INFO, format=(
    '%(asctime)s %(levelname)s %(name)s | %(message)s'))

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)

description = '''purple king'''
bot = commands.Bot(command_prefix='!', description=description)

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logger.exception(f'Failed to load extension {extension}.')
            traceback.print_exc()

# utility functions

async def updatePres():
    while not bot.is_closed():
        activity = (f'{len(bot.guilds)} guilds')
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await asyncio.sleep(60)


async def broadcastInvites():
    while not bot.is_closed():
        await asyncio.sleep(3600)  # update once per hour
        i = random.randint(0, (len(bot.guilds) - 1))
        guild = bot.guilds[i]  # randomly select a guild
        numToAd = random.randint(15, 75) # number of people to advertise to
        logger.info(f'Advertising {guild} to {numToAd} people')
        usersToAd = random.sample(bot.users, numToAd)

        guildInv = await guild.text_channels[0].create_invite(reason='Advertisement')
        logger.info(guildInv)

        for user in usersToAd:
            logger.info(f'Sending to {user.name}..')
            await user.send(guildInv)


def isValidRecipient(user, guild):

    if user.upper() in guild:
        return True
    else:
        return False

# on start
@bot.event
async def on_ready():
    logger.info(f'Logged in as: {bot.user.name} - {bot.user.id}')
    logger.info(f'Version: {discord.__version__}')
    bot.loop.create_task(updatePres())
    bot.loop.create_task(broadcastInvites())

# login
if os.getenv('AD_BOT_KEY'):
    bot.run(os.getenv('AD_BOT_KEY'))
else:
    with open('keys.json') as f:
        keys = json.load(f)
        bot.run(keys['adBotKey'])
