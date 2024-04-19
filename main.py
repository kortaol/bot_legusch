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
    scheduler.add_job(rofl, trigger=CronTrigger(hour="2,12,22", minute=28))
    scheduler.start()

async def rofl():
    for x in channels: 
        ch = bot.get_channel(x)
        await ch.send("хд")

@bot.slash_command(name = "addch", description = "Добавить кАНАЛ, в который будет говориться рофл")
@has_permissions(administrator=True)
async def add_channel( ctx, channel:discord.TextChannel ):
    if channel.id in channels:
        await ctx.respond("Ошибка: канал уже добавлен!", ephemeral = True)
        return
    async with aiofiles.open('channels', 'a') as channels_file:
        await channels_file.write( str(channel.id) + '\n' )
        await channels_file.close()
    channels.append( channel.id )
    await ctx.respond("Канал <#{}> успешно добавлен.".format(channel.id), ephemeral = True)

@bot.slash_command(name = "rmch", description = "Удалить кАНАЛ из списка")
@has_permissions(administrator=True)
async def remove_channel( ctx, channel:discord.TextChannel ):
    if channel.id not in channels:
        await ctx.respond("Ошибка: канал не был добавлен!", ephemeral = True)
        return
    async with aiofiles.open("channels", "r") as f:
        lines = await f.readlines()
    async with aiofiles.open("channels", "w") as f:
        for line in lines:
            if line.strip("\n") != str( channel.id ):
                await f.write(line)


    channels.remove( channel.id )
    await ctx.respond("Канал <#{}> успешно удалён.".format(channel.id), ephemeral = True)

bot.run( token )
