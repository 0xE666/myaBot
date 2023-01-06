import discord, time, sys, os, asyncio, requests, traceback
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db


class guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()

    def timestamp(self):
        return time.strftime('%H:%M:%S')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    async def check_whitelist(self, guild_id) -> bool:
        whitelisted_guilds = self.db.column("SELECT guild_id FROM whitelist")
        if int(guild_id) in whitelisted_guilds:
            return True
        else:
            embed = Embed(title="server not whitelisted",
            description="contact devs: .e#0666 & sin#9876",
            colour=int(self.utility.get_bot_color()))

            channels = []
            for channel in self.bot.get_guild(int(guild_id)).text_channels:
                channels.append(channel.id)

            channel = self.bot.get_channel(int(channels[0]))
            await channel.send(embed=embed)

            await self.bot.get_guild(int(guild_id)).leave()

            return False

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        check = await self.check_whitelist(guild.id)
        if check == True:
            self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", int(guild.id))
        if check == False:
            owner_id = guild.owner_id
            # self.db.execute("INSERT OR IGNORE INTO banned_guilds (guild_id) VALUES (?)", int(guild.id))
            embed = Embed(title='`guild not whitelisted`', color=0x2f3136, timestamp=datetime.utcnow())
            fields = [("guild_owner", f"_{owner_id}_", True),
                    ("guild", f"_{guild.id}_", True)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            channel = self.bot.get_channel(int(self.utility.get_owner_log()))
            await channel.send(embed=embed)

        self.db.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        owner_id = guild.owner_id
        embed = Embed(title='`bot left/kicked from guild`', color=0x2f3136, timestamp=datetime.utcnow())
        fields = [("guild_owner", f"_{owner_id}_", True),
                ("guild", f"_{guild.id}_", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        channel = self.bot.get_channel(int(self.utility.get_owner_log()))
        await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(guild(bot))

        


