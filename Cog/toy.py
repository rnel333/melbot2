import discord
from discord.ext import commands
import random

#emoji
TDEmoji = {"4545":"<:TD_4545:831556271890497586>",
           "ATT":"<:TD_ATT:829508732937437214>",
           "GG":"<:TD_GG:830947631035318293>",
           "HeIs":"<:TD_HeIs:827150581688696852>",
           "WYH":"<:TD_WYH:831116974997897226>",
           "Wkey":"<:TD_Wkey:831115017000714240>",
           "aramu":"<:TD_aramu:835421961852289034>",
           "bath":"<:TD_bath:829576087268753408>",
           "droop":"<:TD_droop:829574120840364083>",
           "minus":"<:TD_giriminus:892836026404454421>",
           "plus":"<:TD_giriplus:832925537852325910>",
           "good":"<:TD_good:829573629451829288>",
           "iam":"<:TD_iam:829835273546104923>",
           "idk":"<:TD_idk:829574733166411776>",
           "judge":"<:TD_judge:831114078486396928>",
           "kekw":"<:TD_kekw:892839023037534348>",
           "meuu":"<:TD_meuu:830062238701977710>",
           "pressure":"<:TD_pressure:831111980445204480>",
           "pretend":"<:TD_pretend:885562573234249758>",
           "question":"<:TD_question:829508716356960266>",
           "ty":"<:TD_ty:830061707765219359>",
           "ungry":"<:TD_ungry:829835850157260800>",
           "kusa":"<:TD_www:836048600416256047>"
           }

EmojiTDivision = "<:TETUDIVISION:886487499382333490>"
EmojiNumber = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':ten:']
TakenakaTetu = ["<:take:895131529905340446>","<:naka:895131584653561906>","<:tetu:895121512821035018>"]

#embed
    #slot
Emoji = [TDEmoji["good"], TDEmoji["GG"], TDEmoji["aramu"], TDEmoji["pressure"], TDEmoji["iam"], TDEmoji["ty"], TDEmoji["ungry"], TDEmoji["kusa"]]
Eslot = [0,0,0]
slot = None
embedSlot = discord.Embed(title="slot",description=("pless" + EmojiTDivision))
embedSlot.add_field(name="1",value=EmojiTDivision)
embedSlot.add_field(name="2",value=EmojiTDivision)
embedSlot.add_field(name="3",value=EmojiTDivision)



class Toy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#commands
    #/slot
    @commands.command()
    async def slot(self, ctx):
        global slot
        slot = await ctx.send(embed=embedSlot)
        await slot.add_reaction(EmojiTDivision)

    #/tetu
    @commands.command()
    async def tetu(self, ctx):
        """竹中哲"""
        await ctx.message.delete()
        await ctx.send(TakenakaTetu[0] + TakenakaTetu[1] + TakenakaTetu[2])


#eventlistener
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = str(payload.emoji)
        user = payload.member

        #slotなら
        if emoji == EmojiTDivision and message == slot:
            print("slot")
            for i in range(3):
                j = random.randrange(0,len(Emoji))
                embedSlot.set_field_at(i,name=i+1,value=Emoji[j])
                Eslot[i] = Emoji[j]
            if(Eslot[0] == Eslot[1] == Eslot[2]):
                embedSlot.color = 0xffff00
            else:
                embedSlot.color = 0x000000
            await message.edit(embed=embedSlot)
            await message.remove_reaction(emoji, user)

def setup(bot):
    return bot.add_cog(Toy(bot))