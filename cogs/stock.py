import json
import logging
import os

import clearbit
import requests

import discord
from discord.ext import commands

IEX_ENDPOINT = 'https://api.iextrading.com/1.0/'

if not os.getenv('BOTKEY'):
    with open(os.path.dirname(__file__) + '/../keys.json') as f:
        keys = json.load(f)
        clearbit.key = keys['clearbitKey']


class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: create a once-per-day updated list of possible symbols, then check against that to see if were doing a company name or ticker
    @commands.command(description='Get info on a stock given a symbol', pass_context=True)
    async def stock(self, ctx, symbol):
        # get stock price
        params = {'symbols': symbol}
        r = requests.get(IEX_ENDPOINT + "/tops/last", params=params)
        iexStock = r.json()[0]

        # get actual company name (this is super janky)
        r = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' +
                         symbol + '&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback')
        yahooStock = r.text
        yahooStock = yahooStock[39:][:-2]
        yahooStock = json.loads(yahooStock)['ResultSet']['Result'][0]

        # get company logo (much less janky)
        clearbitStock = clearbit.NameToDomain.find(name=yahooStock['name'])
        logging.debug(clearbitStock)

        # format embed
        e = discord.Embed(title=yahooStock['name'],
                          type='rich', colour=discord.Colour.teal())
        e.add_field(name='Price', value=iexStock['price'])
        e.set_image(url=clearbitStock['logo'])
        e.set_author(name='stockbot',
                     url='https://github.com/djmango/stockbot',
                     icon_url='https://i.imgur.com/KrYvuxE.png')
        e.set_footer(text='Made in Python with discord.py@rewrite and love <3 and also tears',
                     icon_url='http://i.imgur.com/5BFecvA.png')

        # send
        await ctx.channel.send(embed=e)


def setup(bot):
    bot.add_cog(StockCog(bot))
