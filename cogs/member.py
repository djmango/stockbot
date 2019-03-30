import discord
from discord.ext import commands


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.message.author
        await self.bot.say(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(pass_context=True, name='top_role', aliases=['toprole'])
    async def show_toprole(self, ctx, member: discord.Member = None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.message.author

        await ctx.channel.send(f'The top role for {member.display_name} is {member.top_role.name}')

    @commands.command(pass_context=True, name='perms', aliases=['perms_for', 'permissions'])
    async def check_permissions(self, ctx, member: discord.Member = None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.message.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(
            perm for perm, value in member.server_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(
            title='Permissions for:', description=member.server.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.channel.send(content=None, embed=embed)
        # Thanks to Gio for the Command. idk who gio is but it was in the example, so, congrats gio!


def setup(bot):
    bot.add_cog(MembersCog(bot))
