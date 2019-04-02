import json
import logging
import os

import clearbit
import requests

import discord
from bs4 import BeautifulSoup as Soup
from discord.ext import commands

IEX_ENDPOINT = 'https://api.iextrading.com/1.0/'

logger = logging.getLogger('bot.stock')

if not os.getenv('BOTKEY'):
    with open(os.path.dirname(__file__) + '/../keys.json') as f:
        keys = json.load(f)
        clearbit.key = str(keys['clearbitKey'])


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
        yahooStock = yahooStock[39:][:-2]  # trim the raw text to get just json
        yahooStock = json.loads(yahooStock)['ResultSet']['Result'][0]

        # get company logo (much less janky method)
        clearbitStock = clearbit.NameToDomain.find(name=yahooStock['name'])
        
        if clearbitStock:
            company_logo = clearbitStock['logo']
        else: # if we couldnt find a logo the clean way

            # initialize place for links
            links = []
            num_images = 1 # a suggestion for how many images to get
            
            # step by 100 because each return gives up to 100 links

            query = yahooStock['name'].replace(" ", "")

            for i in range(0, num_images, 100):
                url = 'https://www.google.com/search?q='+query+'logo&safe=strict&client=firefox-b-1-d&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjN1byi_7HhAhWIm1kKHfgeAqMQ_AUIDigB&biw=1536&bih=738&dpr=1.25'

                r = requests.get(url)
                page = r.text

                # use BeautifulSoup to parse as html
                soup = Soup(page, 'html.parser')

                # all img tags, only returns results of search
                imgs = soup.find_all('img')

                # loop through images and put src in links list
                for j in range(len(imgs)):
                    links.append(imgs[j]["src"])

                company_logo = links[0]

        # format embed
        e = discord.Embed(title=yahooStock['name'],
                          type='rich', colour=discord.Colour.teal())
        e.add_field(name='Price', value=iexStock['price'])
        e.set_image(url=company_logo)
        e.set_author(name='stockbot',
                     url='https://github.com/djmango/stockbot',
                     icon_url='https://i.imgur.com/KrYvuxE.png')
        e.set_footer(text='Made in Python with discord.py@rewrite and love <3 and also tears',
                     icon_url='http://i.imgur.com/5BFecvA.png')

        # send
        await ctx.channel.send(embed=e)


def setup(bot):
    bot.add_cog(StockCog(bot))
