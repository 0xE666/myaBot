from ast import Delete
from this import d
from turtle import title
import discord, time, aiohttp
from discord.ext import commands
from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional
import sys, os, asyncio, requests
from io import BytesIO

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from utils import utility
from datetime import datetime

def timestamp():
    return time.strftime('%H:%M:%S')

sniped_message = None
sniped_author = None
sniped_author_id = None

class snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.utility = utility.utility_api()
        self.sniped_message = None
        self.sniped_author = None
        self.sniped_author_id = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author != self.bot.user:
            self.sniped_message = message
            self.sniped_author_id = message.author.id
            self.sniped_author = message.author

    @commands.command(name='snipe', aliases=['s'], description='snipe a deleted message', help='e.g. {prefix}snipe|s')
    async def sniper(self, ctx: commands.Command):

        await asyncio.sleep(1)
        async with ctx.typing():
            await asyncio.sleep(0.3)

            if self.utility.check_white_listed(ctx.author.id):
                if self.sniped_message == None:
                    pass

                if not self.sniped_message.attachments:
                    embed1 = discord.Embed(description=f"\n{self.sniped_message.content}", color=0x2f3136, timestamp=datetime.utcnow())
                    embed1.set_author(name=self.sniped_author.name, icon_url=self.sniped_author.avatar.url)
                    embed1.set_footer(text=f"sniped message by {ctx.author.display_name}#{ctx.author.discriminator}")
                    await ctx.send(embed=embed1)
                    return await ctx.message.delete()

                if self.sniped_message.attachments:
                    new_url = self.sniped_message.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
                    embed = discord.Embed(color=0x2f3136, timestamp=datetime.utcnow())
                    embed.set_image(url=new_url)
                    embed.set_author(name=self.sniped_author.name, icon_url=self.sniped_author.avatar.url)
                    embed.set_footer(text=f"sniped message by {ctx.author.display_name}#{ctx.author.discriminator}")
                    await ctx.send(embed=embed)
                    return await ctx.message.delete()

            else:
                await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(snipe(bot))