import discord
import random
from discord.ext import commands
from custom_functions import ping_cmd, random_cmd

bot = commands.Bot(command_prefix='.')
TOKEN = 'NzA2MTg1MTEzMDU4NDEwNTE2.Xq5MQw.3Y4xZxbw7L7dkBGbQHRBMH5Dv5U'

@bot.event
async def on_ready():
    print(f'Bot is Ready')
    await bot.change_presence(activity=discord.Game('Jadi Admin'))

# async def bot_presence_cycle():
#     await bot.wait_until_ready()

#     while not bot.is_closed():
#         bot_status = random.choice(bot_statuses)
#         await bot.change_presence(activity=discord.Game(bot_status))
#         await asyncio.sleep(120)

@bot.command()
async def ping(ctx):
    response = ping_cmd.ping_info(bot.latency * 1000)
    await ctx.send(response)

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

@bot.command(name='nomor',aliases=['random_number'])
async def _nomor(ctx, *, numbers):
    number = numbers.split(' ')
    if len(number) > 2:
        await ctx.send(f'Error. Too many parameters. Need 2 parameters')
    elif len(number) == 2:
        if str.isdigit(number[0]) and str.isdigit(number[1]):
            response = random_cmd.random_int(int(min(number)),int(max(number)))
        else:
            response = f'Please input numbers only (2 numbers)'
        await ctx.send(response)
    elif len(number) == 1:
        await ctx.send(f'Error. Only 1 parameter given. Need 2 parameters')

@_nomor.error
async def _nomor_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please input 2 numbers (e.g. 1 100)')

@bot.command(name='nanya',aliases=['random_ask'])
async def _nanya(ctx, *, question):
    response = random_cmd.random_ask(question)
    await ctx.send(response)

@_nanya.error
async def _nanya_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter a question')

bot.run(TOKEN)