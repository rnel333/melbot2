import asyncio
import discord
from discord.ext import commands

apikey = 'b9U204z0r906S1d'
userSpeaker = {"おてつ":13, "らいる":4, "ちょう":14, "rnel333":8}

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.message.guild:
            if ctx.author.voice is None:
                await ctx.send('vcに接続してください')
            else:
                if ctx.guild.voice_client:
                    if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                        await ctx.send('接続済みです')
                    else:
                        await ctx.voice_client.disconnect()
                        await asyncio.sleep(0.5)
                        await ctx.author.voice.channel.connect()
                else:
                    await ctx.author.voice.channel.connect()

    @commands.command()
    async def bye(self, ctx):
        if ctx.message.guild:
            if ctx.voice_client is None:
                await ctx.send('vcに接続していません')
            else:
                await ctx.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.voice_client:
            if not message.author.bot:
                if not message.content.startswith('/'):
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
                    
                    name = message.author.name
                    if name in userSpeaker:
                        speaker = userSpeaker[name]
                    else:
                        speaker = 3
                    
                    mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={apikey}&speaker={speaker}&intonationScale=1'
                    while message.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
                await self.bot.process_commands(message)



def setup(bot):
    return bot.add_cog(TTS(bot))