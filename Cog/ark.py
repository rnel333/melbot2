import discord
from discord.ext import commands



class ark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def pet(self, ctx, name="---", level="---", gender="-", health="-", stamina="-", oxygen="-", food="-", weight="-", melee="-"):
        """生物のステータスを登録"""
        await ctx.message.delete()
        embedPet = discord.Embed(title = "DinoStatus")
        embedPet.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embedPet.add_field(name="名前", value=name, inline=False)
        embedPet.add_field(name="レベル", value=level, inline=True)
        embedPet.add_field(name="性別", value=gender, inline=True)
        embedPet.add_field(name="-------------------", value="ステータス", inline=False)
        embedPet.add_field(name="体力", value=health, inline=True)
        embedPet.add_field(name="スタミナ", value=stamina, inline=True)
        embedPet.add_field(name="酸素", value=oxygen, inline=True)
        embedPet.add_field(name="食料", value=food, inline=True)
        embedPet.add_field(name="重量", value=weight, inline=True)
        embedPet.add_field(name="攻撃", value=melee, inline=True)
        await ctx.send(embed=embedPet)
        
async def setup(bot):
    await bot.add_cog(ark(bot))