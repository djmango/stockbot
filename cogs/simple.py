import random

import discord
import logging

from discord.ext import commands


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.

For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/v0.16.12/ext/commands/api.html#checks

You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689

For a list of events:
https://discordpy.readthedocs.io/en/v0.16.12/api.html#event-reference
"""


class SimpleCog(commands.Cog):
    """SimpleCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='repeat', aliases=['copy', 'mimic'])
    async def do_repeat(self, ctx, our_input: str):
        """A simple command which repeats our input. """
        our_input = ctx.message.content
        await ctx.channel.send(our_input)

    @commands.command(name='add', aliases=['plus'], pass_context=True)
    @commands.guild_only()
    async def do_addition(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await ctx.channel.send(f'The sum of **{first}** and **{second}**  is  **{total}**')
    
    @commands.command(pass_context=True, name='info')
    async def info(self, ctx):
        """Custom help command"""
        embed = discord.Embed(title="Type !help command for more info on a command.",
                              description="You can also type !help category for more info on a category.", colour=discord.Colour.purple())
        embed.set_author(name="Commands", icon_url="https://cdn.discordapp.com/attachments/564478629048746004/564526110608719903/icon_2.png")
        embed.add_field(name='joined', value='Says when a member joined', inline=True)
        embed.add_field(name='perms', value='A simple command which checks a members Guild Permissions', inline=True)
        embed.add_field(name='top_role', value='Simple command which shows the members Top Role', inline=True)
        embed.add_field(name='add', value='A simple command which does addition on two integer values', inline=True)
        embed.add_field(name='choose', value='Chooses between multiple choices', inline=True)
        embed.add_field(name='info', value='Custom help command', inline=True)
        embed.add_field(name='me', value='A simple command which only responds to the owner of the bot', inline=True)
        embed.add_field(name='repeat', value='A simple command which repeats our input', inline=True)
        embed.add_field(name='roll', value='Rolls a dice in NdN format', inline=True)
        embed.add_field(name='Help', value='shows this message', inline=True)
        embed.set_footer(text="Command prefix is !, EX: !help")
        await ctx.author.send(embed=embed)

    @commands.command(pass_context=True, name='roll')
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""

        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.channel.send('Format has to be in NdN! Ex: 3d6 = three six-sided dice')
            return

        result = ', '.join(str(random.randint(1, limit))
                           for r in range(rolls))
        await ctx.channel.send(result)

    @commands.command(description='For when you wanna settle the score some other way', pass_context=True, name="choose")
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.channel.send(random.choice(choices))

    async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild.
        For this example I will keep things simple and just log some info.
        Notice how because we are in a cog class we do not need to use @bot.event
        For more information:
        http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_member_ban
        Check above for a list of events.
        """
        logging.info(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')


def setup(bot):
    bot.add_cog(SimpleCog(bot))
