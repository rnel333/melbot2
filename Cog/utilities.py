import asyncio
import discord
from discord.ext import commands
import random
import re

#role
appid = 954592530660466758
testappid = 954607092243763230

#emoji
EmojiNumber = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':ten:']

#embed
    #app
embedApp = discord.Embed(title = "暇なひと～")
embedApp.add_field(name = "募集人数", value = "---", inline=True)
embedApp.add_field(name = "開始時刻", value = "---", inline=True)
embedApp.add_field(name = "参加者", value = None, inline=False)
    #team
embedTeam = discord.Embed(title = "チーム分け")

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#commands
    #/app
    @commands.command(aliases=["app"])
    async def appeal(self, ctx, *args):
        """遊べる人を募集する"""
        global apper,app,react,partList,partUser
        apper = ctx.author.name
        partList = []
        partUser = None
        react = []
        desc = ""
        

        await ctx.message.delete()
        embedApp.set_author(name=apper, icon_url=ctx.author.avatar_url) # 募集者の表示
        # arg[]の内容で処理を分岐
        if args:
            for arg in args:
                if re.match(r'[0-9]{2}:[0-9]{2}', arg): # 時刻の入力
                    embedApp.set_field_at(1, name = "開始時刻", value = arg)
                
                elif re.match(r'^@[0-9]', arg) : # @人数
                    arg = arg.replace('@', '')
                    embedApp.set_field_at(0, name = "募集人数", value = arg + "人")
                
                elif re.match(r'<:([a-zA-Z0-9_]+):\d+>', arg):
                    react.append(arg)
                    desc += arg
                else: # それ以外
                    desc += arg
            embedApp.description = desc
        
        partList.append(apper)
        partUser = '\n'.join(partList)
        embedApp.set_field_at(2, name = "参加者", value = partUser, inline = False)
        
        app = await ctx.send(embed = embedApp)
        if react:
            for reaction in react:
                await app.add_reaction(reaction)
        else:
            await app.add_reaction("✋")
        await app.add_reaction("🚫")
        print(app.reaction)
        
    #/set
    @commands.command()
    async def set(self, ctx, *args):
        """/appを編集"""
        react = []
        desc = ""
        if args:
            for arg in args:
                if re.match(r'[0-9]{2}:[0-9]{2}', arg): # 時刻の入力
                    embedApp.set_field_at(1, name = "開始時刻", value = arg)
                
                elif re.match(r'^@[0-9]', arg) : # @人数
                    arg.replace('@', '')
                    embedApp.set_field_at(0, name = "募集人数", value = arg + "人")
                
                elif re.match(r'<:([a-zA-Z0-9_]+):\d+>', arg):
                    react.append(arg)
                    desc += arg
                else: # それ以外
                    desc += arg
            embedApp.description = desc
            await app.edit(embed = embedApp)
            await app.reactions.clear()

    #/dice
    @commands.command()
    async def dice(self, ctx, *arg):
        """0~10までの数字を出す"""
        await ctx.message.delete()
        n = random.randrange(0,10)
        if len(arg) == 2:
            n = random.randrange(int(arg[0]),int(arg[1]))
        elif len(arg) == 1:
            n = random.randrange(0,int(arg[0]))
        await ctx.send(EmojiNumber[n])

    #/team
    @commands.command()
    async def team(self, ctx):
        """vcに参加中の人をチーム分けする"""
        await ctx.message.delete()
        members = [i.name for i in ctx.author.voice.channel.members]
        random.shuffle(members)
        team_num = 2
        team = []
        for i in range(team_num):
            team.append("====チーム"+str(i+1)+"====")
            team.extend(members[i:len(members):team_num])

        await ctx.send("\n".join(team))





#eventlistener
    #リアクション追加時
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = str(payload.emoji)
        user = payload.member

        if message == app:
            global apper,react,partList,partUser
            #✋ or reactのとき
            if emoji == "✋" or emoji in react:
                #partリスト(参加者)に名前がなければ名前を追加
                if str(user.name) not in partList:
                    partList.append(user.name)
                partUser = '\n'.join(partList)
                embedApp.set_field_at(2, name = "参加者", value = partUser, inline = False)
                await message.edit(embed=embedApp)
            #募集中止
            elif emoji == "🚫" and user.name == apper:
                await message.delete()

async def setup(bot):
    await bot.add_cog(Utilities(bot))