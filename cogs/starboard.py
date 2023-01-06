import discord, time, sys, os, asyncio, requests, traceback, emoji, re, types
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_emoji(reactions, emoji):
    for i in reactions:
        if str(i.emoji) == emoji:
            return i
    return None



class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    def timestamp(self):
        return time.strftime('%H:%M:%S')

    @commands.group(name='starboard', invoke_without_command=True)
    async def starboard(self, ctx: commands.Context):
        starboard_channel = self.db.record("SELECT starboard FROM guilds WHERE guild_id = ?",
        int(ctx.message.guild.id))[0]

        star_emoji = self.db.record("SELECT star_emoji FROM guilds WHERE guild_id = ?",
        int(ctx.message.guild.id))[0]

        star_count = self.db.record("SELECT star_count FROM guilds WHERE guild_id = ?",
        int(ctx.message.guild.id))[0]

        starboard_channel = self.bot.get_channel(int(starboard_channel))

        embed = Embed(title='`success`', description=f"starboard: {starboard_channel.mention}\nstar emoji: {emoji.emojize(star_emoji)}\nstar count: {star_count}", color=0x2f3136, timestamp=datetime.utcnow())
        return await ctx.send(embed=embed, delete_after=30)

    @starboard.command(name='emoji', description='change starboard emoji', help="e.g. {prefix}starboard emoji {emoji}")
    async def starboard_emoji(self, ctx: commands.Context, star_emoji=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):

            if star_emoji is not None:
                demoji = emoji.demojize(star_emoji)
                self.db.execute("UPDATE guilds SET star_emoji = ? WHERE guild_id = ?",
                str(demoji), int(ctx.message.guild.id))[0]
                self.db.commit()
                embed = Embed(title='`success`', description=f"updated starboard emoji to {star_emoji}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

            if star_emoji is None:
                star_emoji = self.db.record("SELECT star_emoji FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]
                star_count = self.db.record("SELECT star_count FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]

                embed = Embed(title='`success`', description=f"star emoji: {emoji.emojize(star_emoji)}\nstar count: {star_count}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @starboard.command(name='count', description='change starboard count', help="e.g. {prefix}starboard count 1|2")
    async def starboard_count(self, ctx: commands.Context, star_count=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):

            if star_count is not None:
                self.db.execute("UPDATE guilds SET star_count = ? WHERE guild_id = ?",
                str(star_count), int(ctx.message.guild.id))
                self.db.commit()
                embed = Embed(title='`success`', description=f"updated starboard count to {star_count}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

            if star_count is None:
                star_count = self.db.record("SELECT star_count FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]
                embed = Embed(title='`success`', description=f"star count: {star_count}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @starboard.command(name='channel', description='change starboard channel', help="e.g. {prefix}starboard channel {channel_id}|{channel_mention}")
    async def starboard_channel(self, ctx: commands.Context, star_channel=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            if star_channel is not None:

                if "#" in star_channel:
                    channel_id = re.findall("<#(\d{15,19})>", star_channel)
                    if channel_id:
                        star_channel = channel_id[0]

                starboard_channel = self.bot.get_channel(int(star_channel))

                if starboard_channel is not None:
                    self.db.execute("UPDATE guilds SET starboard = ? WHERE guild_id = ?",
                    str(starboard_channel.id), int(ctx.message.guild.id))
                    self.db.commit()
                    embed = Embed(title='`success`', description=f"updated starboard channel to {starboard_channel.mention}", color=0x2f3136, timestamp=datetime.utcnow())
                    return await ctx.send(embed=embed, delete_after=30)
                
                if starboard_channel is None:
                    embed = Embed(title='`argument invalid`', color=0x2f3136, timestamp=datetime.utcnow())
                    fields = [("e.g.", f"!starboard channel 1021728944141119570\n!starboard channel `<#1021728944141119570>`", True)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    return await ctx.send(embed=embed, delete_after=30)

            if star_channel is None:
                starboard_channel = self.db.record("SELECT starboard FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]
                starboard_channel_ = self.bot.get_channel(int(starboard_channel))
                embed = Embed(title='`success`', description=f"starboard: {starboard_channel_.mention}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @starboard.command(name='enable', aliases=['on'], description='enable starboard', help='e.g. {prefix}starboard enable|on')
    async def starboard_enable(self, ctx: commands.Context):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            
            current_starboard_bool = self.db.record("SELECT starboard_bool FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]

            self.db.execute("UPDATE guilds SET starboard_bool = ? WHERE guild_id = ?",
                        1, int(ctx.message.guild.id))
            self.db.commit()

            starboard_channel = self.db.record("SELECT starboard FROM guilds WHERE guild_id = ?",
            int(ctx.message.guild.id))[0]
            starboard_channel_ = self.bot.get_channel(int(starboard_channel))
            
            embed = Embed(title='`success`', description=f"starboard enabled.\nstarboard: {starboard_channel_.mention}", color=0x2f3136, timestamp=datetime.utcnow())
            return await ctx.send(embed=embed, delete_after=30)
                        
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @starboard.command(name='disable', aliases=['off'], description='disable starboard', help='e.g. {prefix}starboard disable|off')
    async def starboard_disable(self, ctx: commands.Context, starboard=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            
            current_starboard_bool = self.db.record("SELECT starboard_bool FROM guilds WHERE guild_id = ?",
                int(ctx.message.guild.id))[0]

            self.db.execute("UPDATE guilds SET starboard_bool = ? WHERE guild_id = ?",
                        0, int(ctx.message.guild.id))
            self.db.commit()

            embed = Embed(title='`success`', description=f"starboard disabled.", color=0x2f3136, timestamp=datetime.utcnow())
            return await ctx.send(embed=embed, delete_after=30)
            
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @starboard.command(name='delete', aliases=['erase'], description='delete starboard message', help='e.g. {prefix}starboard delete|erase {id}')
    async def starboard_delete(self, ctx: commands.Context, id):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            
            starboard_message_id = self.db.record("SELECT destination FROM starboard where id=?", int(id))[0]
            try:

                channel = self.bot.get_channel(self.guild_star_channel(ctx.author.guild.id))
                msg = await channel.fetch_message(starboard_message_id)
                await msg.delete()

                self.db.execute("DELETE FROM starboard WHERE id=?",
                int(id))
                self.db.commit()

                embed = Embed(title='`success`', description=f"succesfully deleted\nmessage_id: {starboard_message_id}\nentry: {id}", color=0x2f3136, timestamp=datetime.utcnow())
                return await ctx.send(embed=embed, delete_after=30)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed)

            
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)


    def get_starboard_bool(self, guild_id) -> bool:

        current_starboard_bool = self.db.record("SELECT starboard_bool FROM guilds WHERE guild_id = ?",
                int(guild_id))[0]

        if current_starboard_bool:
            return True

        return False
    
    def guild_starboard_emoji(self, guild_id):
        star_emoji = self.db.record("SELECT star_emoji FROM guilds WHERE guild_id = ?",
                int(guild_id))[0]

        return star_emoji

    def guild_star_count(self, guild_id):
        star_count = self.db.record("SELECT star_count FROM guilds WHERE guild_id = ?",
                int(guild_id))[0]

        return star_count

    def guild_star_channel(self, guild_id):
        star_count = self.db.record("SELECT starboard FROM guilds WHERE guild_id = ?",
                int(guild_id))[0]

        return star_count

    def starboard_id(self, message_id, channel_id):
        starboard_id = self.db.record("SELECT id FROM starboard WHERE message=? and channel=?", message_id, channel_id)
        return starboard_id



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        guild_id = payload.guild_id
        if not self.get_starboard_bool(guild_id):
            return
        
        star_emoji = self.guild_starboard_emoji(guild_id)
        star_emoji = emoji.emojize(star_emoji)
        star_count = self.guild_star_count(guild_id)

        

        if str(payload.emoji) == star_emoji and payload.user_id != self.bot.user.id:

            message = discord.utils.get(self.bot.cached_messages, id=payload.message_id)
            if not message:
                message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

            reaction = get_emoji(message.reactions, str(payload.emoji))
            

            reaction_users = []
            async for x in reaction.users():
                if not x.id == message.author.id:
                    reaction_users.append(x)

            count = len(reaction_users)

            cached = False

            fetch = self.db.record("SELECT destination FROM starboard WHERE message=? and channel=?",
                            payload.message_id, payload.channel_id)

            if fetch:
                star_id = fetch[0]
                if star_id is None:
                    return
                cached = True
            

            if count >= star_count and not cached:
                self.db.execute("INSERT into starboard ( message, channel, destination, timestamp ) VALUES ( ?, ?, ?, ?)",
                                message.id, message.channel.id, 0, self.timestamp())

                self.db.commit()
                
                starboard_id = self.starboard_id(message.id, message.channel.id)

                
                channel = self.bot.get_channel(self.guild_star_channel(guild_id))

                author = message.author
                link = message.jump_url
                embed = discord.Embed(title=f"# {message.channel}", description=message.content, color=0x2f3136)
                embed.set_author(name=f"{author.display_name}#{author.discriminator}", icon_url=author.display_avatar.url)
                embed.add_field(name="\u200b", value=f"[jump to message]({link})")
                embed.set_footer(text=f"#{starboard_id[0]}")

                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                
                msg = await channel.send(
                    f"{star_emoji} #{count}",
                    embed=embed
                )

                self.db.execute("UPDATE starboard SET destination=? WHERE message=?",
                                msg.id, message.id)

                self.db.commit()
                
            elif cached:
                try:
                    msg = await self.bot.get_channel(self.guild_star_channel(guild_id)).fetch_message(star_id)
                    text = f"{star_emoji}" + str(count) + " " + " ".join(msg.content.split(" ")[1:])
                    await msg.edit(content=text)
                except discord.NotFound:
                    self.db.execute("DELETE FROM starboard WHERE message=? and channel=?",
                    payload.message_id, payload.channel_id)
                    self.db.commit()
            

async def setup(bot: commands.Bot):
    await bot.add_cog(starboard(bot))
