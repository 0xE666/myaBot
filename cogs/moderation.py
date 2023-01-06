
from ast import Delete
from unicodedata import category
import discord, time
from discord.ext import commands
from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional
import sys, os, asyncio, requests, humanfriendly
from datetime import datetime, timedelta

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from utils import utility
from datetime import datetime

def timestamp():
    return time.strftime('%H:%M:%S')

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.utility = utility.utility_api()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="lock_channel", aliases=['lockchannel'], description='lock a text channel', help="{prefix}lock_channel|lockchannel")
    async def lock_channel_command(self, ctx: commands.Context, role: discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                overwrite = ctx.channel.overwrites_for(role)
                overwrite.update(send_messages=False, add_reactions=False)
                await ctx.channel.set_permissions(role, overwrite=overwrite)

                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'channel locked',
                    color=discord.Color.green()
                )
                
                return await ctx.send(embed=embed, delete_after=5)
            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="unlock_channel", aliases=['unlockchannel'], description='unlock a text channel', help="{prefix}unlock_channel|unlockchannel")
    async def unlock_channel_command(self, ctx: commands.Context, role: discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                overwrite = ctx.channel.overwrites_for(role)
                overwrite.update(send_messages=True, add_reactions=True)
                await ctx.channel.set_permissions(role, overwrite=overwrite)

                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'channel unlocked',
                    color=discord.Color.green()
                )
                
                return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(manage_channels=True)
    @commands.command(name="hide_channel", aliases=['hidechannel'], description='hide a text channel', help="{prefix}hide_channel|hidechannel")
    async def hide_channel_command(self, ctx: commands.Context, role: discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                overwrite = ctx.channel.overwrites_for(role)
                overwrite.update(view_channel=False)
                await ctx.channel.set_permissions(role, overwrite=overwrite)

                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'channel hidden',
                    color=discord.Color.green()
                )
                
                return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)
    
    @commands.has_permissions(manage_channels=True)
    @commands.command(name="unhide_channel", aliases=['unhidechannel'], description='unhide a text channel', help="{prefix}unhide_channel|unhidechannel")
    async def unhide_channel_command(self, ctx: commands.Context, role: discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                overwrite = ctx.channel.overwrites_for(role)
                overwrite.update(view_channel=True)
                await ctx.channel.set_permissions(role, overwrite=overwrite)

                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'channel unhidden',
                    color=discord.Color.green()
                )
                
                return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)


    @commands.has_permissions(administrator=True)
    @commands.command(name="lock_category", aliases=['lockcategory'], description='lock a category', help="{prefix}lock_category|lockcategory {category_id}")
    async def lock_category_command(self, ctx: commands.Context, category: discord.CategoryChannel, role:discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                channels = category.channels
                for channel in channels:
                    overwrite = ctx.channel.overwrites_for(role)
                    overwrite.update(send_messages=False, add_reactions=False)
                    await ctx.channel.set_permissions(role, overwrite=overwrite)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'category locked',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(administrator=True)
    @commands.command(name="unlock_category", aliases=['unlockcategory'], description='unlock a category', help="{prefix}unlock_category|unlockcategory {category_id}")
    async def unlock_category_command(self, ctx: commands.Context, category: discord.CategoryChannel, role:discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                channels = category.channels
                for channel in channels:
                    overwrite = ctx.channel.overwrites_for(role)
                    overwrite.update(send_messages=True, add_reactions=True)
                    await ctx.channel.set_permissions(role, overwrite=overwrite)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'category unlocked',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)
    
    @commands.has_permissions(administrator=True)
    @commands.command(name="hide_category", aliases=['hidecategory'], description='hide a category', help="{prefix}hide_category|hidecategory {category_id}")
    async def hide_category_command(self, ctx: commands.Context, category: discord.CategoryChannel, role:discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                channels = category.channels
                for channel in channels:
                    overwrite = ctx.channel.overwrites_for(role)
                    overwrite.update(view_channel=False)
                    await ctx.channel.set_permissions(role, overwrite=overwrite)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'category hidden',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(administrator=True)
    @commands.command(name="unhide_category", aliases=['unhidecategory'], description='unhide a category', help="{prefix}unhide_category|unhidecategory {category_id}")
    async def unhide_category_command(self, ctx: commands.Context, category: discord.CategoryChannel, role:discord.Role=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                if ctx.author.bot:
                    return
                
                if role == None:
                    role = ctx.guild.default_role

                channels = category.channels
                for channel in channels:
                    overwrite = ctx.channel.overwrites_for(role)
                    overwrite.update(view_channel=True)
                    await ctx.channel.set_permissions(role, overwrite=overwrite)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'category shown',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)


    @commands.has_permissions(moderate_members=True)
    @commands.command(name="unmute", description='unmute a user', help="{prefix}unmute {user}")
    async def unmute_command(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            try:
                bot = ctx.guild.get_member(self.bot.user.id)
                if reason == None:
                    reason = 'n/a'
                if not ctx.author.top_role.position > member.top_role.position:
                    return await ctx.reply('you do not have permission to do that')
                
                if not bot.top_role.position > member.top_role.position:
                    return await ctx.reply('i dont have permission to do this')
                
                elif member == ctx.author:
                    return await ctx.reply('you cant use commands on yourself')

                else:
                    role = discord.utils.get(ctx.guild.roles, name="muted")
                    await member.remove_roles(role)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'unmuted {member}\nreason: {reason}',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)
    
    @commands.has_permissions(moderate_members=True)
    @commands.command(name="mute", description='mute a user', help="{prefix}mute {user}")
    async def mute_command(self, ctx: commands.Context, member: discord.Member=None, *, reason=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            if member == None:
                em = discord.Embed(title="command: **mute**", description="aliases : `mute`\nusage : `-mute @member`\ne.g. : `-mute @.e#0666`", color=0x2f3136)
                return await ctx.send(embed=em, delete_after=10)

            try:
                bot = ctx.guild.get_member(self.bot.user.id)
                if reason == None:
                    reason = 'n/a'

                if not ctx.author.top_role.position > member.top_role.position:
                    return await ctx.reply('you do not have permission to do that')
                
                if not bot.top_role.position > member.top_role.position:
                    return await ctx.reply('i dont have permission to do this')

                elif member == ctx.author:
                    return await ctx.reply('you cant use commands on yourself')

                else:
                    role = discord.utils.get(ctx.guild.roles, name="muted")
                    await member.add_roles(role)

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'muted {member}\nreason: {reason}',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)
            except commands.MissingRequiredArgument:
                command = discord.Embed(title="**Command: mute**",description=f"\nmutes the mentioned user from the guild:\n```syntax: ,mute (user) <reason>\nexample: ,mute .e#2991 fuck you```", color=0x2f3136, timestamp=datetime.utcnow())
                await ctx.send(embed=command, delete_after=5)
            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(kick_members=True)
    @commands.command(name="kick", description='kick a user', help="{prefix}kick {user}")
    async def kick_command(self, ctx: commands.Context, member: discord.Member=None, *, reason=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):
            if member == None:
                em = discord.Embed(title="command: **kick**", description="aliases : `kick`\nusage : `-kick @member`\ne.g. : `-kick @.e#0666`", color=0x2f3136)
                return await ctx.send(embed=em, delete_after=10)
            try:
                bot = ctx.guild.get_member(self.bot.user.id)
                if reason == None:
                    reason = 'n/a'

                if not ctx.author.top_role.position > member.top_role.position:
                    return await ctx.reply('you do not have permission to do that')
                
                if not bot.top_role.position > member.top_role.position:
                    return await ctx.reply('i dont have permission to do this')

                elif member == ctx.author:
                    return await ctx.reply('you cant use commands on yourself')

                else:
                    embed = self.utility.create_embed(
                        ctx.author,
                        title="you've been kicked",
                        description=f'by: <@{ctx.author.id}>\nreason: {reason}',
                        color=discord.Color.red()
                    )

                    await member.send(embed)
                    await ctx.guild.kick(member, reason=reason)
                    

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'kicked {member}\nreason: {reason}',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

    @commands.has_permissions(ban_members=True)
    @commands.command(name="ban", description='ban a user', help="{prefix}ban {user}")
    async def ban_command(self, ctx: commands.Context, member: discord.Member=None, *, reason=None):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        
        if self.utility.check_white_listed(ctx.author.id):

            if member == None:
                em = discord.Embed(title="command: **ban**", description="aliases : `ban`\nusage : `-ban @member`\ne.g. : `-ban @.e#0666`", color=0x2f3136)
                return await ctx.send(embed=em, delete_after=10)

            try:
                bot = ctx.guild.get_member(self.bot.user.id)
                if reason == None:
                    reason = 'n/a'

                if not ctx.author.top_role.position > member.top_role.position:
                    return await ctx.reply('you do not have permission to do that')
                
                if not bot.top_role.position > member.top_role.position:
                    return await ctx.reply('i dont have permission to do this')

                elif member == ctx.author:
                    return await ctx.reply('you cant use commands on yourself')

                else:
                    embed = self.utility.create_embed(
                        ctx.author,
                        title="you've been banned",
                        description=f'by: <@{ctx.author.id}>\nreason: {reason}',
                        color=discord.Color.red()
                    )

                    await member.send(embed=embed)
                    await ctx.guild.ban(member, reason=reason)
                    

                    embed = self.utility.create_embed(
                        ctx.author,
                        title='success',
                        description=f'banned {member}\nreason: {reason}',
                        color=discord.Color.green()
                    )
                    
                    return await ctx.send(embed=embed, delete_after=5)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)

async def setup(bot: commands.Bot):
    await bot.add_cog(moderation(bot))

