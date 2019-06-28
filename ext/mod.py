import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        '''Kicks `member`'''
        await member.kick()
        await ctx.send("__**Successfully User" + member + "Has Been Kicked!**__")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        '''Bans `member`'''
        await member.ban()
        await ctx.send("__**Successfully User" + member + " Has Been Banned!**__")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        '''Mutes `member`
    You need to have role called `Muted` with right permissions to make this command work'''
        role = await discord.utils.get(ctx.guild.roles, name='Muted')
        # TODO


def setup(bot):
    bot.add_cog(Moderation(bot))