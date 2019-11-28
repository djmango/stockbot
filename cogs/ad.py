import json
import logging
import os
import threading

import discord
from pathlib import Path
from discord.ext import commands

logger = logging.getLogger('bot.ad')

# utility functions


if not os.getenv('BROADCAST_PASS'):
    with open(os.getcwd() + '/keys.json') as f:
        keys = json.load(f)
        broadcastPass = str(keys['broadcastPass'])

# actual cog class


class AdCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def ad(self, ctx):
        """ enable your server for advertising """

        # if the command was invoked by the guild owner
        if ctx.author.id is ctx.guild.owner.id:
            with open(os.getcwd() + '/guildsToAdvertise.json', 'r') as f:
                guildsToAdvertise = json.load(f)

            # make sure the guilds not already in the list
            if ctx.guild.id in guildsToAdvertise:
                await ctx.channel.send('Yer guilds already being advertised, dimwit')
            else:
                with open(os.getcwd() + '/guildsToAdvertise.json', 'w') as f:
                    guildsToAdvertise.append(ctx.guild.id)
                    print(guildsToAdvertise)
                    json.dump(guildsToAdvertise, f)
                    await ctx.channel.send('Yer being advertised now buddy')
        else:
            await ctx.channel.send('Yer not the owner, you stupid bean')

    @commands.command(pass_context=False)
    async def dmall(self, passwd, *msg):
        """ dm all """
        msg = msg[1:]
        fullMsg = ' '.join(msg)
        
        logger.debug(fullMsg)
        if passwd == broadcastPass:
            for user in self.bot.users:
                try:
                    pass
                    await user.send(fullMsg)
                except:
                    pass


def setup(bot):
    bot.add_cog(AdCog(bot))
