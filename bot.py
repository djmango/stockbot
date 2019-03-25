#!/usr/bin/env python3

""" the stock bot """

import json
import logging
import os
import random

import discord
import requests
from discord.ext import commands

# consts
IEX_ENDPOINT = 'https://api.iextrading.com/1.0/'

# setup

logging.basicConfig(level=logging.INFO)
description = '''possibly the most stupid bot to have ever been created'''
bot = commands.Bot(command_prefix='sb!', description=description)
discord.ext.commands.group(name='stocks')

# on start
@bot.event
async def on_ready():
    logging.info('Logged in as' + bot.user.name)
    logging.info(bot.user.id)
    logging.info('------')
    await bot.change_presence(game=discord.Game(name='sb! | the stock bot | @djmango'))

# on member join
@bot.event
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

# commands
@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command(pass_context=True)
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN! Ex: 3d6 = three six-sided dice')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way', group='Other')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

# TODO: create a once-per-day updated list of possible symbols
@bot.command(description='Get info on a stock given a symbol', group='Stocks', pass_context=True)
async def stock(ctx, symbol):
    # get stock price
    params = {'symbols': symbol}
    r = requests.get(IEX_ENDPOINT + "/tops/last", params=params)
    iexStock = r.json()[0]

    # get actual company name
    r = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' +
                     symbol + '&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback')
    yahooStock = r.text
    yahooStock = yahooStock[39:][:-2]
    yahooStock = json.loads(yahooStock)['ResultSet']['Result'][0]

    # TODO: logo pulling, more rich embed stuff
    # format embed
    e = discord.Embed(title=yahooStock['name'],
                      type='rich', colour=discord.Colour.teal())
    e.add_field(name='Price', value=iexStock['price'])

    # send
    await bot.send_message(destination=ctx.message.channel, embed=e)

# login
if os.getenv('BOTKEY'):
    bot.run(os.getenv('BOTKEY'))
else:
    with open('keys.json') as f:
        keys = json.load(f)
        bot.run(keys['botKey'])
