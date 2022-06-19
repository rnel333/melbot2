import asyncio
import discord
from discord.ext import commands

apikey = 'b9U204z0r906S1d'
userSpeaker = {"412118891381391363":13, "313221694946803722":0, "502836827712126986":14, "265185184356237314":13, "502037256832286722":10}

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
        #print(message.channel.id)
        if message.author.voice:
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

                        id = message.author.id
                        if id in userSpeaker:
                            speaker = userSpeaker[id]
                        else:
                            speaker = 3
                    
                    
                    #print(id, speaker)
                    mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={apikey}&speaker={speaker}&intonationScale=1'
                    while message.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
                await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if before.channel is None:
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                await after.channel.connect()
            else:
                if member.guild.voice_client.channel is after.channel:
                    text = member.name + "が入室しました"
                    mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={apikey}&speaker=3&intonationScale=1'
                    while member.guild.voice_client.is_playing():
                        await asyncio.sleep(0.5)
                    source = await discord.FFmpegOpusAudio.from_probe(mp3url)
                    member.guild.voice_client.play(source)
        elif after.channel is None:
            if member.guild.voice_client:
                if member.guild.voice_client.channel is before.channel:
                    if len(member.guild.voice_client.channel.members) == 1:
                        await asyncio.sleep(0.5)
                        await member.guild.voice_client.disconnect()
                    else:
                        text = member.name + 'さんが退室しました'
                        mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={apikey}&speaker=3&intonationScale=1'
                        while member.guild.voice_client.is_playing():
                            await asyncio.sleep(0.5)
                        source = await discord.FFmpegOpusAudio.from_probe(mp3url)
                        member.guild.voice_client.play(source)
        elif before.channel != after.channel:
            if member.guild.voice_client:
                if member.guild.voice_client.channel is before.channel:
                    if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                        await asyncio.sleep(0.5)
                        await member.guild.voice_client.disconnect()
                        await asyncio.sleep(0.5)
                        await after.channel.connect()


def setup(bot):
    return bot.add_cog(TTS(bot))