import discord
import random
import os
import json
import asyncio
import pytz
from pytz import timezone
from datetime import datetime, timedelta
from discord.ext import commands

import rw_json
from custom_functions import ping_cmd, random_cmd, string_cmd

def get_prefix(client, message):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    return servers[str(message.guild.id)]['prefix']

bot = commands.Bot(command_prefix=get_prefix)
TOKEN = os.environ.get('BOT_TOKEN')

@bot.event
async def on_ready():
    print(f'Bot is Ready')

bot_statuses = ['Admin','Satpam','Guru']
async def bot_presence_cycle():
    await bot.wait_until_ready()

    while not bot.is_closed():
        bot_status = random.choice(bot_statuses)
        await bot.change_presence(activity=discord.Game('jadi ' + bot_status))
        await asyncio.sleep(120)

@bot.command()
async def ping(ctx):
    response = ping_cmd.ping_info(bot.latency * 1000)
    await ctx.send(response)

# ---------- Add server ids and prefixes to json ---------- #

@bot.event
async def on_guild_join(guild):
    servers = rw_json.open_json('servers.json')
    servers[str(guild.id)] = {'server_id' : str(guild.id), 'server_name': str(guild.name),'prefix': '.', 'channels_aliases':dict()}
    rw_json.write_json('servers.json',servers)

@bot.event
async def on_guild_remove(guild):
    servers = rw_json.open_json('servers.json')
    servers.pop(str(guild.id))
    rw_json.write_json('servers.json',servers)

@commands.has_permissions(administrator=True)
@bot.command()
async def changeprefix(ctx, prefix):
    servers = rw_json.open_json('servers.json')
    servers[str(ctx.guild.id)]['prefix'] = prefix
    rw_json.write_json('servers.json',servers)

# ---------- End Add server ids and prefixes to json ---------- #

# -------------------- Self role -------------------- #

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    servers = rw_json.open_json('servers.json')
    ROLE_MESSAGE_ID = servers[str(payload.guild_id)]['role_message_id']
    if message_id == int(ROLE_MESSAGE_ID):
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
        if payload.emoji.name == '🟧': # I had to use this since I used bot message and built-in emoji for choosing role
            role = discord.utils.get(guild.roles, name='SMP')
        elif payload.emoji.name == '🟦': # I had to use this since I used bot message and built-in emoji for choosing role
            role = discord.utils.get(guild.roles, name='SD')
        else:
            role = None
            print(f'Role not found for {payload.emoji.name}')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f'Done! {member} added to role {role}')
            else:
                print('Member not found!')
        else:
            print('Role not found!')

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    servers = rw_json.open_json('servers.json')
    ROLE_MESSAGE_ID = servers[str(payload.guild_id)]['role_message_id']
    if message_id == int(ROLE_MESSAGE_ID):
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🟧': # I had to use this since I used bot message and built-in emoji for choosing role
            role = discord.utils.get(guild.roles, name='SMP')
        elif payload.emoji.name == '🟦': # I had to use this since I used bot message and built-in emoji for choosing role
            role = discord.utils.get(guild.roles, name='SD')
        else:
            role = None
            print(f'Role not found for {payload.emoji.name}')

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f'Done! {member} removed from role {role}')
            else:
                print('Member not found!')
        else:
            print('Role not found!')

@commands.has_permissions(administrator=True)
@bot.command('choose_role')
async def _choose_role(ctx):
    servers = rw_json.open_json('servers.json')
    msg = string_cmd.get_response('choose_role')
    message = await ctx.send(msg)
    message_id = message.id
    servers[str(ctx.guild.id)]['role_message_id'] = str(message_id)
    await message.add_reaction('🟦')
    await message.add_reaction('🟧')

    rw_json.write_json('servers.json',servers)

# -------------------- End self role -------------------- #

# -------------------- Owner's Commands -------------------- #

@commands.has_permissions(administrator=True)
@bot.command()
async def clear(ctx, limits=5):
    await ctx.channel.purge(limit=limits)

@commands.has_permissions(administrator=True)
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked because : {reason}')

@commands.has_permissions(administrator=True)
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned because : {reason}')

@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'User {user.mention} has been unbanned.')
            return

# ----- Set, Get, and Delete custom alias for a channel ------ #

@commands.has_permissions(administrator=True)
@bot.command('channels_aliases')
async def _set_channel(ctx):
    servers = rw_json.open_json('servers.json')
    channel_aliases = list(servers[str(ctx.guild.id)]['channels_aliases'].keys())
    await ctx.send(f'`Your custom channels aliases are : {channel_aliases}. You can find them by typing .get_channel channel_alias`')

@commands.has_permissions(administrator=True)
@bot.command('set_channel')
async def _set_channel(ctx, purpose):
    servers = rw_json.open_json('servers.json')
    servers[str(ctx.guild.id)]['channels_aliases'][purpose] = str(ctx.channel.id)
    rw_json.write_json('servers.json',servers)
    await ctx.send(f'`You have set this channel as {purpose} channel`')

@commands.has_permissions(administrator=True)
@bot.command('delete_channel')
async def _delete_channel(ctx, purpose):
    servers = rw_json.open_json('servers.json')
    if purpose in servers[str(ctx.guild.id)]['channels_aliases'].keys():
        del servers[str(ctx.guild.id)]['channels_aliases'][purpose]
        rw_json.write_json('servers.json',servers)
        await ctx.send(f'`You are no longer have {purpose} channel now`')
    else:
        await ctx.send(f"`You haven't set a channel as {purpose} channel`")

@commands.has_permissions(administrator=True)
@bot.command('get_channel')
async def _get_channel(ctx, purpose):
    servers = rw_json.open_json('servers.json')
    this_server = servers[str(ctx.guild.id)]
    if purpose in this_server['channels_aliases']:
        channel = bot.get_channel(int(this_server['channels_aliases'][purpose]))
        await ctx.send(f'{channel.mention} is your {purpose} channel')
    else:
        await ctx.send(f"`You haven't set a channel as {purpose} channel`")

@commands.has_permissions(administrator=True)
@bot.command('send_channel')
async def _send_channel(ctx, *, message):
    servers = rw_json.open_json('servers.json')
    purpose = message.split(' ')
    try: 
        channel_id = servers[str(ctx.guild.id)]['channels_aliases'][purpose[0]]
        if channel_id != '' or channel_id is not None:
            channel = bot.get_channel(int(channel_id))
            response = purpose[1:].copy()
            await channel.send(' '.join(map(str, response)))
        else:
            response = f"`Key not found in json for {purpose[0]} channel`"
            await ctx.send(response)
    except:
        response = f"`You haven't set a channel as {purpose[0]} channel. Please enter a channel and type .set_channel {purpose[0]}`"
        await ctx.send(response)
    
# ------------- End custom alias for a channel -------------- #

@commands.has_permissions(administrator=True)
@bot.command('pesan')
async def _pesan(ctx, pesan):
    response = string_cmd.get_response(pesan)
    await ctx.send(response)

@commands.has_permissions(administrator=True)
@bot.command('perbaikan')
async def _perbaikan(ctx):
    perbaikan = string_cmd.get_response('perbaikan')
    await ctx.send(perbaikan)
    await ctx.send(embed=discord.Embed().set_image(url='https://i.imgflip.com/3oct0x.png'))

# ------------------- End Owner's commands ------------------- #

# -------------------- Member's commands -------------------- #

@bot.command('time')
async def _time(ctx, country):
    base_zone = timezone('Asia/Jakarta')
    city = None
    for x in pytz.all_timezones:
        if str.lower(country) in str.lower(x):
            city = x
    if city is not None:
        your_zone = timezone(city)
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        base_dt = base_zone.localize(datetime.now())
        your_dt = base_dt.astimezone(your_zone)   
        await ctx.send(f'Current time in {city} : {str(your_dt.strftime(fmt))}')
    else:
        await ctx.send('Your city is not registered in current list')

@bot.command(name='angka',aliases=['random_number'])
async def _angka(ctx, *, numbers):
    number = numbers.split(' ')
    if len(number) > 2:
        await ctx.send(f'Error. Tidak ada angka. Tulis 2 angka')
    elif len(number) == 2:
        if str.isdigit(number[0]) and str.isdigit(number[1]):
            response = random_cmd.random_int(int(min(number)),int(max(number)))
        else:
            response = f'Tulis angka saja (2 angka)'
        await ctx.send(response)
    elif len(number) == 1:
        await ctx.send(f'Error. Hanya ada 1 angka. Tulis 2 angka')

@_angka.error
async def _angka_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Tulis 2 angka (contoh: .angka 1 100)')

@bot.command(name='nanya',aliases=['random_ask'])
async def _nanya(ctx, *, question):
    response = random_cmd.random_ask(question)
    await ctx.send(response)

@_nanya.error
async def _nanya_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Tulis apa aja (contoh: .nanya apa kabar)')

@bot.command(name='dadu')
async def _dadu(ctx, member : discord.User):
    await ctx.send(f'🎲 {ctx.message.author.mention} melempar {member.mention} {random.randint(1,6)}')

@_dadu.error
async def _dadu_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'🎲 {ctx.message.author.mention} melempar {random.randint(1,6)}')

# -------------------- End Member's commands -------------------- #
bot.loop.create_task(bot_presence_cycle())
bot.run(TOKEN)