import discord
from discord.ext import commands

class CogTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        await ctx.send('にゃーん')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

def setup(bot):
    return bot.add_cog(CogTest(bot))