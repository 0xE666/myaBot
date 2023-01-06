import ios, discord, os, datetime, requests, json, time, ast, re, inspect
from db import db
from glob import glob
from asyncio import sleep
from utils import utility
from discord.ui import Button, View
from discord.ext import commands, tasks
from discord.ext.commands import Context
from datetime import datetime, timedelta
from discord import Embed, File, DMChannel
from discord.ext.commands import Bot as bot_base
from apscheduler.triggers.cron import CronTrigger
from discord.errors import HTTPException, Forbidden
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import when_mentioned_or, command, has_permissions
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)

db_manager = db.database_manager()
utility_api = utility.utility_api()

COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("-")(bot, message)
    prefix = db_manager.record("SELECT prefix FROM guilds WHERE guild_id=?", int(message.guild.id))[0]
    return commands.when_mentioned_or(prefix)(bot,message)

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=get_prefix,
    case_insensitive=True,
    intents=intents,
    help_command=None
)

bot.remove_command("help")
start_time = time.time()


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

def update_db():
    db_manager.multiexec("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)",
                ((int(guild.id),) for guild in bot.guilds))
    db_manager.commit()

async def check_whitelist(guild_id):
    whitelisted_guilds = db_manager.column("SELECT guild_id FROM whitelist")
    if int(guild_id) in whitelisted_guilds:
        pass
    else:
        embed = Embed(title="server not whitelisted",
        description="contact dev: .e#0666",
        colour=int(utility_api.get_bot_color()))

        channels = []
        for channel in bot.get_guild(int(guild_id)).text_channels:
            channels.append(channel.id)
        
        channel = bot.get_channel(int(channels[0]))
        await channel.send(embed=embed)

        await bot.get_guild(int(guild_id)).leave()

@bot.event
async def on_ready():
    await load_extensions()
    status_log = bot.get_channel(1046140877740965888)
    print('-' * 30)
    status_msg = f"{bot.user} is ready with {len(bot.commands)} commands in {len(bot.guilds)} servers"
    print(status_msg)
    print('-' * 30)
    await status_log.send(embed=discord.Embed(title="status", description=status_msg, color=0x2f3136, timestamp=datetime.utcnow()))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="-help"))
    for guild in bot.guilds:
        await check_whitelist(guild.id)

    update_db()
    
def upt():
    seconds = time.time() - start_time
    hour = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    day = hour * 24
    return "\🟢 Online For `%02dD %02dH %02dM`" % (day, hour, mins)

@bot.command()
async def uptime(ctx):
    if utility_api.check_white_listed(ctx.author.id):
        await ctx.send(embed=upt())
    else:
        await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)




bot.run(utility_api.get_bot_token())