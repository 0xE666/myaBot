
from ast import Delete
import discord, time
from discord.ext import commands
from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional
import sys, os, asyncio, requests

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from utils import utility
from datetime import datetime

def timestamp():
    return time.strftime('%H:%M:%S')

class basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.utility = utility.utility_api()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')
    
    
    @commands.command(name='invite', aliases=['inv'], description='generate invite link for server', help='{prefix} invite|inv')
    async def invite_command(self, ctx: commands.Context):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        try:
            invite_link = await ctx.channel.create_invite()
            await ctx.send(invite_link, delete_after=10)

        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    @commands.command(name='avatar_lookup', aliases=['avatar', 'pfp'], description='lookup user profile picture', help='{prefix} pfp|avatar {mention}|user-id')
    async def pfp_lookup(self, ctx: commands.Context, *, user: Optional[Union[discord.Member, discord.User, str]]):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        try:
            user: discord.User = user or ctx.author

            r = requests.get(user.display_avatar.url)
            if r.status_code == 200:
                with open("data/images/image1.png", 'wb') as f:
                    f.write(r.content)

            channel = ctx.channel
            embed = self.utility.create_embed(
                ctx.author,
                title=f"{user}'s avatar",
                url=f"{user.display_avatar.url}",
                thumbnail=user.display_avatar,
                color=0x2f3136
            )
            file = discord.File("data/images/image1.png", filename="image1.png")
            embed.set_image(url="attachment://image1.png")

            await ctx.send(file=file, embed=embed, delete_after=30)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)


    @commands.command(name='member', aliases=['lookup', 'search'], description='lookup discord user', help='{prefix} lookup|search {mention}|user-id')
    async def user(self, ctx: commands.Context, *, user: Optional[Union[discord.Member, discord.User, str]]):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        user: Union[discord.Member, discord.User, str] = user or ctx.author

        if isinstance(user, str):
            raise commands.UserNotFound(user)

        fetched = user if user.banner else await self.bot.fetch_user(user.id)

        flags = [name.replace('_', ' ').title() for name, value in dict.fromkeys(iter(user.public_flags)) if value]
        badges = '\n'.join(flags) or 'none'

        embed = discord.Embed(title=f"**{user}**",
            color=0x2f3136)
        embed.set_image(url=fetched.banner)
        embed.set_thumbnail(url=fetched.avatar.url)

        embed.add_field(
            name='**general:**',
            value=f'**user-id:** {user.id}\n'
                  f'**creation date:** {self.utility.user_friendly_dt(user.created_at)}\n'
                  f'**badges:** {badges}',
            inline=False
        )

        if isinstance(user, discord.Member) and user.guild == ctx.guild:
            role_mentions = self.utility.shorten_below_number(
                [role.mention for role in reversed(user.roles)][:-1],
                separator=' ',
                number=500
            )
            top_role = user.top_role.mention if user.top_role != ctx.guild.default_role else 'no roles'

            embed.add_field(
                name='**member:**',
                value=f'**nickname:** {user.nick or "no nickname"}\n'
                      f'**joined sever at:** {self.utility.user_friendly_dt(user.joined_at)}\n'
                      f'**highest role:** {top_role}\n'
                      f'**roles:** {role_mentions or "no roles"}',
                inline=False
            )

            await ctx.send(embed=embed)
        
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

    @commands.command(aliases=['guild', 'server'], help="displays guild information e.g. !server|guild")
    @commands.guild_only()
    async def server_command(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild

        bot_count = sum(member.bot for member in guild.members)

        embed = self.utility.create_embed(
            ctx.author,
            title=f'**info for {guild.name}**',
            thumbnail=guild.icon,
            image=guild.banner,
            color=0x2f3136
        )

        features = []
        if 'COMMUNITY' in guild.features:
            features.append('community')
        if 'VERIFIED' in guild.features:
            features.append(f'verified')
        if 'PARTNERED' in guild.features:
            features.append(f'partnered')
        if 'DISCOVERABLE' in guild.features:
            features.append(f'discoverable')
        if not features:
            features.append('no special features')

        embed.add_field(
            name='**general**:',
            value=f'description: {guild.description or "no description"}\n'
                  f'owner: {guild.owner} ({guild.owner_id})\n'
                  f'id: {guild.id}\n'
                  f'creation date: {self.utility.user_friendly_dt(guild.created_at)}',
            inline=False
        )

        embed.add_field(name='**special features**', value=', '.join(features))

        embed.add_field(
            name=f'**boost**',
            value=f'boost level: {guild.premium_tier} \n'
                  f'amount of boosters: {guild.premium_subscription_count}\n'
                  f'booster Role: '
                  f'{guild.premium_subscriber_role.mention if guild.premium_subscriber_role else "none"}',
            inline=False
        )

        embed.add_field(
            name='**counts**',
            value=f'Members: {guild.member_count} total members\n'
                  f'{guild.member_count - bot_count} humans; {bot_count} bots\n'
                  f'roles: {len(guild.roles)} roles\n'
                  f'text channels: {len(guild.text_channels)} channels\n'
                  f'voice Channels: {len(guild.voice_channels)} channels\n'
                  f'emotes: {len(ctx.guild.emojis)} emotes',
            inline=False
        )

        embed.add_field(
            name='**security**',
            value=f'2fa required?: {"yes" if guild.mfa_level else "no"}\n'
                  f'verification level: {str(guild.verification_level).replace("_", " ").title()}\n'
                  f'nsfw filter: {str(guild.explicit_content_filter).replace("_", " ").title()}'
        )

        await ctx.send(embed=embed, delete_after=30)


    @commands.command(name='embed', description='embed a message', help='{prefix}embed {message}')
    async def embed_command(self, ctx: commands.Context, *, message):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        channel = ctx.channel
        embed = self.utility.create_embed(
            ctx.author,
            title=f"{message}",
            color=0x2f3136
        )
        await ctx.send(embed=embed, delete_after=10)

    @commands.command(name='embed_stay', description='embed a message', help='{prefix}embed_stay {message}')
    async def embed_command1(self, ctx: commands.Context, *, message):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        channel = ctx.channel
        embed = self.utility.create_embed(
            ctx.author,
            title=f"{message}",
            color=0x2f3136
        )
        await ctx.send(embed=embed)
        
    @commands.command(name='imbed', description='embed a image', help='{prefix} {image}')
    async def imbed_command(self, ctx: commands.Context, *, message):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        r = requests.get(message)
        if r.status_code == 200:
            with open("data/images/image.png", 'wb') as f:
                f.write(r.content)

        channel = ctx.channel
        embed = discord.Embed(color=0x2f3136)
        file = discord.File("data/images/image.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed, delete_after=30)

    @commands.command(name='imbed_stay', description='embed a image', help='{prefix} {image}')
    async def imbed_command1(self, ctx: commands.Context, *, message):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(1.5)

        r = requests.get(message)
        if r.status_code == 200:
            with open("data/images/image.png", 'wb') as f:
                f.write(r.content)

        channel = ctx.channel
        embed = discord.Embed(color=0x2f3136)
        file = discord.File("data/images/image.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file, embed=embed)

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='purge', aliases=['clear'], description='purge bulk messages', help='{prefix}purge|clear [int]\n e.g. {prefix}clear 50')
    async def clear_command(self, ctx: commands.Context, amount: int):
        try:
            if ctx.author.bot:
                return

            if amount == None:
                amount = 10

            await ctx.channel.purge(limit=amount)
            return await ctx.send(f"{ctx.author.mention}, successfully purged {amount} messages", delete_after=5)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    

async def setup(bot: commands.Bot):
    await bot.add_cog(basic(bot))
