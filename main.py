from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import aiofiles

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix='!', help_command=commands.DefaultHelpCommand(), intents=discord.Intents.default())

token = open('token', 'r').readline()
channels_file = open('channels')
channels = channels_file.readlines()
if len(channels):
    channels = [ int(x) for x in channels ]
channels_file.close()

@bot.event
async def on_ready():
    print("Connected!")
    scheduler = AsyncIOScheduler()
    ch = bot.get_channel(1086755221755138141)
    scheduler.add_job(rofl, trigger=CronTrigger(hour="2,12,22", minute=28))
    scheduler.start()

async def rofl():
    for x in channels: 
        ch = bot.get_channel(x)
        await ch.send("хд")

@bot.slash_command(name = "addch", description = "Добавить кАНАЛ, в который будет говориться рофл")
@has_permissions(administrator=True)
async def add_channel(ctx, channel:discord.TextChannel ):
    async with aiofiles.open('channels', 'a') as channels_file:
        await channels_file.write( str(channel.id) + '\n' )
        await channels_file.close()
    channels.append( channel.id )
    await ctx.respond("Канал {} успешно добавлен.".format(channel.name), ephemeral = True)

@bot.slash_command(name = "clch", description = "Очистить список кАНАЛОВ полностью")
@has_permissions(administrator=True)
async def clear_channels( ctx ):
    async with aiofiles.open('channels', 'w') as channels_file:
        await channels_file.close()
    channels = []
    await ctx.respond("Список каналов полностью очищен.", ephemeral = True)

bot.run( token )
