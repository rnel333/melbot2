import discord
from discord.ext import commands
import traceback

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
f = open('TOKEN.txt','r')
TOKEN = f.read()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', help_command=JpHelp(), intents=intents)

#読み込むcogのパスを格納しておく
Cog_pass = [
    "Cog.utilities",
    "Cog.toy",
    "Cog.server",
    "Cog.TTS"
]
#cogのロード
for cog in Cog_pass:
    bot.load_extension(cog)

#


#bot起動時にコンソールに表示
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#botの起動
bot.run(TOKEN)