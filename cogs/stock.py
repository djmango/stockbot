import json
import logging
import os
import threading
import time

import clearbit
import requests
from bs4 import BeautifulSoup as Soup

import discord
from pathlib import Path
from discord.ext import commands

IEX_ENDPOINT = 'https://api.iextrading.com/1.0/'

logger = logging.getLogger('bot.stock')

if not os.getenv('BOTKEY'):
    with open(os.getcwd() + '/keys.json') as f:
        keys = json.load(f)
        clearbit.key = str(keys['clearbitKey'])

# utility functions

def updateSymbolList():
    while True:
        # get json
        r = requests.get(IEX_ENDPOINT + "/tops/")
        iexStock = r.json()

        # grab only symbols
        symbolList = []
        for stock in iexStock:
            symbolList.append(stock['symbol'])

        # write to file
        with open(os.getcwd() + '/symbolList.json', 'w+') as f:
            json.dump(symbolList, f)

        time.sleep(3600)  # update once per hour


def isValidSymbol(symbol):
    with open(os.getcwd() + '/symbolList.json', 'r') as f:
        symbolList = json.load(f)

    if symbol.upper() in symbolList:
        return True
    else:
        return False


updateSymbolListThread = threading.Thread(target=updateSymbolList)

# actual cog class
class StockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Get info on a stock given a symbol', pass_context=True)
    async def stock(self, ctx, symbol):

        if isValidSymbol(symbol):
            # get stock price
            params = {'symbols': symbol}
            r = requests.get(IEX_ENDPOINT + "/tops/last", params=params)
            iexStock = r.json()[0]

            # get actual company name (this is super janky)
            r = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=' +
                             symbol + '&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback')
            yahooStock = r.text
            # trim the raw text to get just json
            yahooStock = yahooStock[39:][:-2]
            yahooStock = json.loads(yahooStock)['ResultSet']['Result'][0]

            # get company logo (much less janky method)
            clearbitStock = clearbit.NameToDomain.find(name=yahooStock['name'])

            if clearbitStock:
                companyLogo = clearbitStock['logo']
            else:  # if we couldnt find a logo the clean way, we can use my janky way

                links = []  # initialize place for links

                query = yahooStock['name'].replace(
                    " ", "")  # cant have spaces in query
                url = 'https://www.google.com/search?q='+query + \
                    'logo&safe=strict&client=firefox-b-1-d&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjN1byi_7HhAhWIm1kKHfgeAqMQ_AUIDigB&biw=1536&bih=738&dpr=1.25'

                r = requests.get(url)
                page = r.text

                # use BeautifulSoup to parse as html
                soup = Soup(page, 'html.parser')

                # all img tags, only returns results of search
                imgs = soup.find_all('img')

                # loop through images and put src in links list
                for j in range(len(imgs)):
                    links.append(imgs[j]["src"])

                companyLogo = links[0]

            # format embed
            e = discord.Embed(title=yahooStock['name'],
                              type='rich', colour=discord.Colour.teal())
            e.add_field(name='Price', value=iexStock['price'])
            e.set_author(name=symbol.upper(),
                         url='https://github.com/djmango/stockbot',
                         icon_url=companyLogo)
            e.set_footer(text='Made in Python with discord.py@rewrite and love and also tears',
                         icon_url='https://i.imgur.com/KrYvuxE.png')

            # send
            await ctx.channel.send(embed=e)
        else:
            await ctx.channel.send('Not a valid symbol')


def setup(bot):
    bot.add_cog(StockCog(bot))
    updateSymbolListThread.daemon = True
    updateSymbolListThread.start()
