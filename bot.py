import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
from discord import app_commands

#####BOT TOKEN#####
load_dotenv()
TOKEN = os.environ['TOKEN']
#####BOT TOKEN#####

ttsapikey = "b9U204z0r906S1d"
ttsids = {412118891381391363:13, 313221694946803722:0, 502836827712126986:14, 265185184356237314:13, 502037256832286722:10}
ttsChannel = ""
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

#####TTS#####
@tree.command(
    name = "join",
    description = "ボイスチャットに接続します"
)
async def join(ctx:discord.Interaction):
    global ttsChannel
    if ctx.user.voice is None:
        await ctx.response.send_message("vcに接続してください", ephemeral=True)
    else:
        if ctx.client.voice_clients:
            if ctx.user.voice.channel == ctx.client.voice_clients.channel:
                await ctx.response.send_message("接続済みです", ephemeral=True)
            else:
                await ctx.user.voice.channel.disconnect()
                await asyncio.sleep(0.5)
        await ctx.user.voice.channel.connect()
        ttsChannel = ctx.channel_id
        await ctx.response.send_message("接続しました", ephemeral=True)

@tree.command(
    name = "bye",
    description = "ボイスチャットから切断します"
)
async def bye(ctx:discord.Interaction):
    global ttsChannel
    await ctx.client.voice_clients[0].disconnect()
    await ctx.response.send_message("切断しました", ephemeral=True)
    ttsChannel = None
#####TTS#####

#####EVENT LISTENER#####
@client.event
async def on_message(message):
    print(type(message.author))
    if message.channel.id == ttsChannel:   # 送信先は読み上げチャンネルに設定されているか
        if client.voice_clients:   # botがvcに存在するか
            if message.author.voice:   # 送信者がvcに存在するか
                print(message.author.id)
                text = message.content
                text = text.replace('\n','、')

                if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                    while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                        text = text[:-1]
                    text = text[:-1] + '、ワラ'

                if text[-1:] == '哲':
                    while text[-2:-1] == '哲':
                        text = text[:-1]
                    text = text[:-1] + 'テツ'

                if message.author.id in ttsids:
                    speaker = ttsids[message.author.id]
                else:
                    speaker = 3

                print(speaker)
                mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={ttsapikey}&speaker={speaker}&intonationScale=1'
                while client.voice_clients[0].is_playing():
                    await asyncio.sleep(0.5)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
#####EVENT LISTENER#####

#####BOT LANCH#####
@client.event
async def on_ready():
    await tree.sync()
    print("ready")
client.run(TOKEN)
#####BOT LANCH#####

