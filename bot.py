import asyncio
import discord
from discord.ext import commands
import traceback
import os
from dotenv import load_dotenv


#/help
class JpHelp(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンドの一覧を表示"

    def get_ending_note(self):
        return ("")

#token
load_dotenv()
TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', help_command=JpHelp(), intents=intents)

#読み込むcogのパスを格納しておく
Cog_pass = [
    "Cog.utilities",
    "Cog.toy",
    "Cog.server",
    "Cog.TTS",
    "Cog.ark"
]

#bot起動時にコンソールに表示
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#botの起動
async def main():
    async with bot:
        for cog in Cog_pass:
            await bot.load_extension(cog)
        await bot.start(TOKEN)
asyncio.run(main())