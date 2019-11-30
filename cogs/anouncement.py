import random


import discord
import logging

from discord.ext import commands


logger = logging.getLogger('bot.anouncement')

roleList = {"ADMIN": "499747726393606155",
            "Zapier": "509942281600499713",
            "DEV": "649484731938897931",
            "MANAGEMENT": "557942021600444416",
            "MODERATORS": "499748283971797003",
            "HOST": "500163662108033024",
            "YEARLY": "516886662194921474",
            "MONTHLY": "516886464219316235",
            "TRIAL (1day)": "515630909043769354",
            "NBT": "528463922265718805",
            "UPside": "631685888702939136",
            "GUEST": "635366680075436061",
            "MD": "642794931542556682",
            "Titan": "643314708228866051",
            "EOD EMAILS": "643320697892110363",
            "DIAMOND": "646600308532838400", }

canYellList = {"ADMIN": "499747726393606155",
               "Zapier": "509942281600499713",
               "DEV": "649484731938897931",
               "MANAGEMENT": "557942021600444416",
               "MODERATORS": "499748283971797003", }
""" I AM YELLING REALLY LOUDLY """


def canYell(userHighestRole):
    if userHighestRole in canYellList.keys():
        return True
    else:
        return False


class AnouncementCog(commands.Cog):
    """AnouncementCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='dmall', aliases=['anounce', 'yell'])
    async def dmall(self, ctx, *msg):
        """ dm all """
        msg = msg[1:]
        fullMsg = ' '.join(msg)
        ctx.author.send('okay, sending the message master ;)')

        for user in self.bot.users:
            try:
                logger.debug('yelling at ' + user.name)
                await user.send(fullMsg)
            except:
                logger.debug('cant yell at ' + user.name)
                pass
    
    @commands.command(pass_context=True, name='dmrole')
    @commands.guild_only()
    async def dmrole(self, ctx, *msg):
        fullMsg = ' '.join(msg[1:])

        # get all members
        members = ctx.guild.members

        # from all members, get the ones with the roles we want
        for role in ctx.message.role_mentions:
            for member in members:
                if role in member.roles:
                    try:
                        logger.debug('yelling at ' + member.name)
                        await member.send(fullMsg)
                    except:
                        logger.debug('cant yell at ' + member.name)
                        pass


    @commands.command(name='add', aliases=['plus'], pass_context=True)
    @commands.guild_only()
    async def do_addition2(self, ctx, first: int, second: int):
        """A simple command which does addition on two integer values."""

        total = first + second
        await ctx.channel.send(f'The sum of **{first}** and **{second}**  is  **{total}**')

    @commands.command(pass_context=True, name='roll')
    async def roll2(self, ctx, dice: str):
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
    async def choose2(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.channel.send(random.choice(choices))


def setup(bot):
    bot.add_cog(AnouncementCog(bot))
