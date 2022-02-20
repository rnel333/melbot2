import discord
from discord.ext import commands

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#minecraft
    @commands.group()
    async def mc(self, ctx):
        """<open/stop/add>"""
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send("/mc <open/stop/add>")
    @mc.command()
    async def open(self, ctx):
        await ctx.message.delete()
        await ctx.send("マイクラあいてるよ～")
        await self.bot.change_presence(activity=discord.Game(f"minecraft"))
    @mc.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        await ctx.send("マイクラとじたよ～")
        await self.bot.change_presence(activity=discord.Game(f"てつのカメラ目線集"))
    @mc.command()
    async def add(self, ctx):
        await ctx.message.delete()
        await ctx.send("マイクラmod増えた～\nhttps://docs.google.com/spreadsheets/d/1qk27GSOn5XY6fuJ2AirVn3mOjoCD5DREw_f97TzQwgg/edit?usp=sharing")

#ark
    @commands.group()
    async def ark(self, ctx):
        """<open/stop/add>"""
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send('/ark <open/stop>')
    @ark.command()
    async def open(self, ctx):
        await ctx.message.delete()
        await ctx.send('ARKあいてるよ～')
        await self.bot.change_presence(activity=discord.Game(f"ARK:Survival Evolved"))
    @ark.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        await ctx.send('ARKとじたよ～')
        await self.bot.change_presence(activity=discord.Game(f"てつのカメラ目線集"))


def setup(bot):
    return bot.add_cog(Server(bot))