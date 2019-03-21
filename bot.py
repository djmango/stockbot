#!/usr/bin/env python3

""" the stock bot """

import logging
import os
import discord
from discord.ext import commands
import random
import json

logging.basicConfig(level=logging.INFO)
description = '''possibly the most stupid bot to have ever been created'''
bot = commands.Bot(command_prefix='sb!', description=description)

@bot.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info('------')
    await bot.change_presence(game=discord.Game(name='sb! | the stock bot | djmango'))

@bot.event
async def on_member_join(member):
    # get guild object
    guild = bot.get_server('435855020462964747')

    # randomize role
    r = random.randint(0, 3)
    if r == 0:
        role = discord.utils.get(guild.roles, name='Farmer')
        await bot.add_roles(member, role)
    elif r == 1:
        role = discord.utils.get(guild.roles, name='Doctor')
        await bot.add_roles(member, role)
    elif r == 2:
        role = discord.utils.get(guild.roles, name='Military')
        await bot.add_roles(member, role)
    elif r == 3:
        role = discord.utils.get(guild.roles, name='Worker')
        await bot.add_roles(member, role)
    
@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

bot.run(os.getenv('BOTKEY'))
