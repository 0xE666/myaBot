import discord, time, sys, os, asyncio, requests, traceback, emoji, re, types
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db


class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    def timestamp(self):
        return time.strftime('%H:%M:%S')

    @commands.group(name='prefix', invoke_without_command=True)
    async def prefix(self, ctx: commands.Context):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
            
        prefix = self.db.record("SELECT prefix FROM guilds WHERE guild_id=?", int(ctx.guild.id))[0]
        embed = Embed(description=f"\ncurrent prefix:    **{prefix}**", color=0x2f3136, timestamp=datetime.utcnow())
        embed.set_footer(text=f"{ctx.author.display_name}#{ctx.author.discriminator}",  icon_url=ctx.author.display_avatar)
        await ctx.send(embed=embed, delete_after=5)

    @prefix.command(name='change', description='change guild prefix', help="e.g. {prefix}prefix change ,")
    async def change(self, ctx: commands.Context, prefix):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            if len(prefix) > 4:
                return await ctx.send(f"{ctx.author.mention}, guild prefix cant be more than 4 characters.", delete_after=5)

            self.db.execute("UPDATE guilds SET prefix=? WHERE guild_id=?",
            prefix, ctx.guild.id)
            self.db.commit()
            embed = Embed(description=f"\nnew prefix:    **{prefix}**", color=0x2f3136, timestamp=datetime.utcnow())
            embed.set_footer(text=f"{ctx.author.display_name}#{ctx.author.discriminator}",  icon_url=ctx.author.display_avatar)
            await ctx.send(embed=embed, delete_after=5)

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(prefix(bot))
