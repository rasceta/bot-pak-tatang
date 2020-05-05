import discord
import random
import os
import json
import asyncio
from discord.ext import commands
from custom_functions import ping_cmd, random_cmd

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

# -------------------- Add server ids and prefixes to json -------------------- #

@bot.event
async def on_guild_join(guild):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    
    servers[str(guild.id)] = {'server_id' : str(guild.id), 'server_name': str(guild.name),'prefix': '.'}

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    
    servers.pop(str(guild.id))

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

@bot.command()
async def changeprefix(ctx, prefix):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    
    servers[str(ctx.guild.id)]['prefix'] = prefix

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

# -------------------- End Add server ids and prefixes to json -------------------- #

# -------------------- Self role -------------------- #

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    with open('servers.json', 'r') as f:
        servers = json.load(f)
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
    with open('servers.json', 'r') as f:
        servers = json.load(f)
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

@commands.has_role('Owner')
@bot.command('choose_role')
async def _choose_role(ctx):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    msg = '''
**Pilih Role: Kelas**
Silakan react berdasarkan kelas kalian untuk mendapatkan role.

>>> :orange_square: = SMP

:blue_square: = SD

'''
    message = await ctx.send(msg)
    message_id = message.id
    servers[str(ctx.guild.id)]['role_message_id'] = str(message_id)

    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)

# -------------------- End self role -------------------- #

# -------------------- Owner's Commands -------------------- #

@commands.has_role('Owner')
@bot.command()
async def clear(ctx, limits=5):
    await ctx.channel.purge(limit=limits)

@commands.has_role('Owner')
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked because : {reason}')

@commands.has_role('Owner')
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned because : {reason}')

@commands.has_role('Owner')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'User {user.mention} has been unbanned.')
            return 

@commands.has_role('Owner')
@bot.command('peraturan')
async def _peraturan(ctx):
    peraturan = '''

**Peraturan Discord Server AHA**
```
- Pilih role sesuai kelas kalian di #📝⫶pendaftaran
- Respect everyone.
- Gunakan channel dengan tepat: 
    •Kategori 💬Berpesan untuk ngobrol menggunakan teks saja. 
    Jika ingin ngobrol dengan sesama teman kelas, masuk kelasnya 
    masing-masing ya
    •Kategori 🏢Fasilitas untuk fasilitas lainnya didukung oleh 
    bot di setiap channelnya (out of topic dan random)
    •Kategori 🔊Bersuara untuk ngobrol dengan suara
- No NSFW, SARA content
```
Udah itu dulu ya. Terima kasih.
    '''
    await ctx.send(peraturan)

@commands.has_role('Owner')
@bot.command('selamat_datang')
async def _selamat_datang(ctx):
    pesan = '''
**Selamat datang di server AHA**
dimana server ini bukanlah official server dari sekolah kita tercinta.
```
- Untuk memulai, pilih kelas (SD/SMP) kalian masing-masing. 
- Jika kalian dari SD dan juga SMP AHA, kalian bisa pilih kedua 
kelas (SD/SMP) tersebut.
- Untuk peraturan dan pengumuman bisa kalian lihat di channel 
#📢⫶pengumuman.
```
Selamat bergabung!:confetti_ball:

    '''
    await ctx.send(pesan)

# -------------------- End Owner's commands -------------------- #

# -------------------- Member's commands -------------------- #

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
async def _dadu(ctx):
    member = ctx.message.author.name
    await ctx.send(f'🎲 {member} melempar {random.randint(1,6)}')

# -------------------- End Member's commands -------------------- #
bot.loop.create_task(bot_presence_cycle())
bot.run(TOKEN)