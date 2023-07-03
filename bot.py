import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from dotenv import load_dotenv
import asyncio
import paramiko

#####BOT TOKEN#####
load_dotenv()
TOKEN = os.environ['TOKEN']
MY_GUILD_ID = os.environ['MY_GUILD_ID']
#####BOT TOKEN#####

#####ENV#####
SERVER_IP = os.environ['SERVER_IP']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

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

#####ROLE MANAGER#####
@tree.command(
    name='role',
    description='ロールを設定します'
)
@app_commands.guilds(
    discord.Object(MY_GUILD_ID)
)
async def role(ctx:discord.Interaction):
    embedCreate(ctx)
    global embedroles
    global msgrls
    global editor
    editor = ctx.user
    print(embedroles.fields)
    length = len(embedroles.fields)
    embedroles.add_field(name="⛔",value="終了")
    await ctx.response.send_message(embed=embedroles)
    msgrls = await ctx.original_response()
    for i in range(length):
        await msgrls.add_reaction(NumToEmoji[i+1])
    await msgrls.add_reaction("⛔")


NumToEmoji = { 0:"0️⃣", 1:"1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣", 6:"6️⃣", 7:"7️⃣", 8:"8️⃣", 9:"9️⃣", 10:"🔟"}
def embedCreate(ctx):
    guild = ctx.guild
    userRoles =[]
    for userRole in ctx.user.roles:
        if userRole.is_assignable():
            roleMention = userRole.mention
            userRoles.append(roleMention)
    print("-----userRoles-----")
    print(userRoles)
    global reactions
    global roles
    reactions = {}
    roles = {}
    for role in guild.roles:
        if role.is_assignable():
            roles[role] = role.mention
    print("-----roles-----")
    print(roles)
    for i,role in enumerate(roles.keys()):
        reactions[NumToEmoji[i+1]] = role
    print("-----reactions-----")
    print(reactions)
    global embedroles
    embedroles = discord.Embed(title="RoleManager",description="あなたの現在のロール\n" + " ".join(userRoles))
    embedroles.clear_fields
    for i,role in enumerate(roles.values()):
        embedroles.add_field(name=NumToEmoji[i+1], value=role,inline=False)
#####ROLE MANAGER#####


#####SERVER MANAGER#####
@tree.command(
    name = 'start',
    description='マインクラフトサーバーを起動します'
)
async def start(ctx:discord.Interaction):
    await ctx.response.send_message('起動します', ephemeral=True)
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SERVER_IP, username=USERNAME, password=PASSWORD)
        stdin, stdout, stderr = ssh.exec_command('screen -r minecraft ; cd /usr/games/minecraft ; java -Xms1G -Xmx4G -jar minecraft_server.jar')
        for o in stdout:
            print('[std]1', o, end='')
            if('Done' in o):
                await ctx.followup.send('起動が完了しました', ephemeral=True)
        if stderr:
            await ctx.followup.send('起動に失敗しました')
#####SERVER MANAGER#####

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

@client.event
async def on_reaction_add(reaction, user):
    global msgrls
    global editor
    global reactions
    global roles
    emoji = reaction.emoji
    if user.bot:
            return
    if reaction.message == msgrls:
        if user == editor:
            if reaction.emoji == "⛔":
                await msgrls.delete()
                return
            if user.get_role(reactions[emoji].id):
                await user.remove_roles(reactions[emoji])
            else:
                await user.add_roles(reactions[emoji])
        await reaction.remove(user)

@client.event
async def on_member_update(before, after):
    global editor
    if before == editor:
        if before.roles != after.roles:
            global msgrls
            await msgrls.edit(embed=embedReload(after))
def embedReload(user):
    global embedroles
    userRoles = []
    for userRole in user.roles:
        if userRole.is_assignable():
            roleMention = userRole.mention
            userRoles.append(roleMention)
    embedroles.description = user.mention + "の現在のロール\n" + " ".join(userRoles)
    return embedroles
#####EVENT LISTENER#####

#####BOT LANCH#####
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(MY_GUILD_ID))
    print("-----")
    print(client.user.name)
    print("ready")
    print("-----")
client.run(TOKEN)
#####BOT LANCH#####
