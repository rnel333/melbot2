from ntpath import join
import random
import discord
from discord.ext import commands

#emoji
EmojiNumber = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':ten:']

#embed
    #app
embedApp = discord.Embed(title = "今日暇なひと～")
embedApp.add_field(name=":o:",value=None)
embedApp.add_field(name=":x:",value=None)
    #team
embedTeam = discord.Embed(title = "チーム分け")

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#commands
    #/app
    @commands.command(aliases=["app"])
    async def appeal(self, ctx, *arg):
        """遊べる人を募集する"""
        global oList,xList,oUser,xUser,apper
        oList = []
        xList = []
        oUser = None
        xUser = None
        apper = ctx.author.name
        await ctx.message.delete()
        embedApp.set_author(name=apper, icon_url=ctx.author.avatar_url)
        embedApp.set_field_at(0,name=":o:",value=oUser)
        embedApp.set_field_at(1,name=":x:",value=xUser)
        if arg:
            embedApp.description = arg[0]
        else:
            embedApp.description = "なんかしよ"
        global app
        app = await ctx.send(embed=embedApp)
        await app.add_reaction("⭕")
        await app.add_reaction("❌")

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
            global oList,xList,oUser,xUser,apper
            #⭕のとき
            if emoji == "⭕":
                #xリストに名前があればリアクションと名前を消す
                if str(user.name) in xList:
                    xList.remove(user.name)
                    if len(xList) > 0:
                        xUser = '\n'.join(xList)
                    else:
                        xUser = None
                    await message.remove_reaction("❌", user)
                    embedApp.set_field_at(1,name=":x:", value=xUser)
                #oリストに名前がなければ名前を追加
                if str(user.name) not in oList:
                    oList.append(user.name)
                oUser = '\n'.join(oList)
                embedApp.set_field_at(0,name=":o:", value=oUser)
                await message.edit(embed=embedApp)
             #❌のとき
            elif emoji == "❌":
                #oリストに名前があればリアクションと名前を消す
                if str(user.name) in oList:
                    oList.remove(user.name)
                    if len(oList) > 0:
                        oUser = '\n'.join(oList)
                    else:
                        oUser = None
                    await message.remove_reaction("⭕",user)
                    embedApp.set_field_at(0,name=":o:",value=oUser)
                #xリストに名前がなければ名前を追加
                if str(user.name) not in xList:
                    xList.append(user.name)
                xUser = '\n'.join(xList)
                embedApp.set_field_at(1,name=":x:",value=xUser)
                await message.edit(embed=embedApp)
            #募集中止
            elif emoji == "🚫" and user.name == apper:
                await message.delete()

def setup(bot):
    return bot.add_cog(Utilities(bot))