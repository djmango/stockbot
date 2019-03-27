import discord
import requests
from discord.ext import commands
import json

IEX_ENDPOINT = 'https://api.iextrading.com/1.0/'

class StocksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: create a once-per-day updated list of possible symbols
    @commands.command(description='Get info on a stock given a symbol', group='Stocks', pass_context=True)
    async def stock(self, ctx, symbol):
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
        await self.bot.send_message(destination=ctx.message.channel, embed=e)


def setup(bot):
    bot.add_cog(StocksCog(bot))
