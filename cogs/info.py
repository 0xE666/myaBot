import discord, time, sys, os, asyncio, requests, traceback, emoji, re, types
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel
from time import time
from psutil import Process, virtual_memory
from datetime import datetime, timedelta
from platform import python_version
from discord import __version__ as discord_version

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db


class info_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()

    def timestamp(self):
        return time.strftime('%H:%M:%S')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')
    
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
                start = time()
                message = await ctx.send(f"latency: {self.bot.latency*1000:,.0f} ms.", delete_after=30)
                end = time()
                await  message.edit(content=f"latency: {self.bot.latency*1000:,.0f} ms, response time: {(end-start)*1000:,.0f} ms")

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @commands.command(name="stats")
    async def stats(self, ctx: commands.Context):
        
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            embed = Embed(title="bot stats",
            color=0x2f3136,
            timestamp=datetime.utcnow())
            proc = Process()
            with proc.oneshot():
                uptime = timedelta(seconds=time()-proc.create_time())
                cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
                mem_total = virtual_memory().total / (1024**2)
                mem_of_total = proc.memory_percent()
                mem_usage = mem_total * (mem_of_total / 100)
                
                
            fields = [
                ("bot_version", self.utility.get_bot_version(), True),
                ("python", python_version(), True),
                ("discord.py", discord_version, True),
                ("uptime", uptime, True),
                ("cpu time", cpu_time, True),
                ("memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} mib ({mem_of_total:.0f}%)", True),
                ("guilds", f"{len(self.bot.guilds)}", True)
                ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await ctx.send(embed=embed, delete_after=30)

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(info_cog(bot))