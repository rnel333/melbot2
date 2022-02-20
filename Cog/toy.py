import discord
from discord.ext import commands
import random

#emoji
EmojiGood = "<:good:829573629451829288>"
Emoji4545 = "<:4545:831556271890497586>"
EmojiGg = "<:GG:830947631035318293>"
EmojiWkey = "<:Wkey:831115017000714240>"
EmojiQuestion = "<:__:829508716356960266>"
EmojiAramu = "<:aramu:835421961852289034>"
EmojiAtu = "<:atu:831111980445204480>"
EmojiDknow = "<:dontknow:829574733166411776>"
EmojiPlus = "<:giri:832925537852325910>"
EmojiIppou = "<:ippou_takenaka:829508732937437214>"
EmojiKaicho = "<:kaichouyazo:829835273546104923>"
EmojiMeuu = "<:meuu:830062238701977710>"
EmojiNaetawa = "<:naetawa:829574120840364083>"
EmojiTakemita = "<:takenakahamita:831113307980562432>"
EmojiTy = "<:thankyou:830061707765219359>"
EmojiOko = "<:ungry:829835850157260800>"
EmojiKusa = "<:wwwww:836048600416256047>"
EmojiTDivision = "<:TETUDIVISION:886487499382333490>"
EmojiNumber = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:',':nine:',':ten:']
TakenakaTetu = ["<:take:895131529905340446>","<:naka:895131584653561906>","<:tetu:895121512821035018>"]

#embed
    #slot
Emoji = [EmojiGood,EmojiGg,EmojiAramu,EmojiAtu,EmojiKaicho,EmojiTy,EmojiOko,EmojiKusa]
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