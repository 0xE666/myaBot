import discord, time, sys, os, asyncio, requests, traceback
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()

    def timestamp(self):
        return time.strftime('%H:%M:%S')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')
    
    @commands.command(name="set_prefix", aliases=["change_prefix", "pre"], description="change server prefix", help="{prefix}prefix !")
    async def change_prefix(self, ctx: commands.Context, prefix):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
                self.db.execute("UPDATE guilds SET prefix=? WHERE guild_id=?",
                str(prefix), int(ctx.author.guild.id))
                self.db.commit()
                embed = Embed(title='`success`', description=f"prefix changed to {prefix}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(misc(bot))