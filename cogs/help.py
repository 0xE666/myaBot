from discord.ext import commands
from asyncio import TimeoutError
from discord.ui import Button, View
from discord import Forbidden, HTTPException
import discord, time, sys, os, asyncio, requests
from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional
from cogs.moderation import moderation

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from utils import utility
from datetime import datetime
from db import db

utility_api = utility.utility_api()
db_manager = db.database_manager()


ebtn = Button(label="e-e.tools", url="https://e-e.tools")
hel_p = f"• prefix - `-`\n• `help <command | category>`\n\n"
helpemb = discord.Embed(title="help menu", description=f"{hel_p}**__categories__\n\ndev\n\nbasic\n\nmoderation\n\nbasic\n\njail\n\ninfo\n\nstarboard\n\nsms\n\nsnipe**", color=0x2f3136)
devemb = discord.Embed(description=f"{hel_p}__**dev**__\n`load_cogs`, `unload_cogs`, `reload_cogs`, `reload_all_cogs`, `prefix`, `setup_moderation`", color=0x2f3136)
modemb = discord.Embed(description=f"{hel_p}__**moderation**__\n`ban`, `kick`, `mute`, `unmute`, `purge`, `lock_channel`, `unlock_channel`, `lock_category`, `unlock_category`, `hide_channel`, `unhide_channel`, `hide_category`, `unhide_category`", color=0x2f3136)
basicemb = discord.Embed(description=f"{hel_p}__**basic**__\n`avatar`, `embed`, `embed_stay`, `clear`, `imbed`, `invite`, `member`, `server_command`", color=0x2f3136)
jailemb = discord.Embed(description=f"{hel_p}__**jail**__\n`jail`, `unjail`", color=0x2f3136)
infoemb = discord.Embed(description=f"{hel_p}__**info**__\n`ping`, `stats`", color=0x2f3136)
staremb = discord.Embed(description=f"{hel_p}__**starboard**__\n`starboard`, `starboard emoji`, `starboard count`, `starboard channel`, `starboard enable`, `starboard disable`, `starboard delete`", color=0x2f3136)
smsemb = discord.Embed(description=f"{hel_p}__**sms**__\n`sms`, `number`", color=0x2f3136)
snipeemb = discord.Embed(description=f"{hel_p}__**snipe**__\n`snipe`", color=0x2f3136)

class Dropdown(discord.ui.Select):
    def __init__(self):
        self.utility = utility.utility_api()

        options = [
            discord.SelectOption(label='dev', description="select for developer commands"),
            discord.SelectOption(label='basic', description="select for basic commands"),
            discord.SelectOption(label='moderation', description="select for moderation commands"),
			discord.SelectOption(label='jail', description="select for jail commands"),
			discord.SelectOption(label='starboard', description="select for starboard commands"),
			discord.SelectOption(label='info', description="select for info commands"),
			discord.SelectOption(label='sms', description="select for info commands"),
            discord.SelectOption(label='snipe', description="select for info commands")
        ]

        super().__init__(placeholder='choose command category...', min_values=1, max_values=1, options=options)

    async def callback(self, interation: discord.Interaction):
        if self.values[0] == "dev":
            await interation.response.edit_message(embed=devemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "basic":
            await interation.response.edit_message(embed=basicemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "moderation":
            await interation.response.edit_message(embed=modemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "jail":
            await interation.response.edit_message(embed=jailemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "starboard":
            await interation.response.edit_message(embed=staremb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "info":
            await interation.response.edit_message(embed=infoemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "sms":
            await interation.response.edit_message(embed=smsemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))
        if self.values[0] == "snipe":
            await interation.response.edit_message(embed=snipeemb.set_thumbnail(url=interation.guild.icon.url).set_footer(text=f"invoked by {interation.user}", icon_url=interation.user.display_avatar))

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


class helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        if ctx.author.bot:
            return

        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        try:

            opts = [ebtn]
            view = DropdownView()
            for opt in opts:
                view.add_item(opt)

            msg = await ctx.send(embed=helpemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    @help.group(invoke_without_command=True)
    async def dev(self, ctx):
        
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)

        if self.utility.check_white_listed(ctx.author.id):
            try:
                view = View()
                buttons = [ebtn]
                for button in buttons:
                    view.add_item(button)
                
                await ctx.send(embed=devemb.set_thumbnail(url=ctx.guild.icon.url), view=view)

            except Exception as e:
                embed = self.utility.format_error(ctx.author, e)
                return await ctx.send(embed=embed, delete_after=90)
        else:
            await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)


    @help.group(invoke_without_command=True)
    async def basic(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=basicemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    @help.group(invoke_without_command=True)
    async def moderation(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=modemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    @help.group(invoke_without_command=True)
    async def jail(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=jailemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    @help.group(invoke_without_command=True)
    async def starboard(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=staremb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)
	
    @help.group(invoke_without_command=True)
    async def info(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=infoemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)
	
    @help.group(invoke_without_command=True)
    async def sms(self, ctx):
        try:
            view = View()
            buttons = [ebtn]
            for button in buttons:
                view.add_item(button)
            
            await ctx.send(embed=smsemb.set_thumbnail(url=ctx.guild.icon.url), view=view)
        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

    
    # ########################################### dev related #######################################

    # @help.command()
    # async def load_cogs(self, ctx):
    #     em = discord.Embed(description="aliases : `load_cogs`, `load_cog`, `lc`\nusage : `load_cog <cog>`\ne.g. : `-load_cog moderation`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    # @help.command()
    # async def unload_cogs(self, ctx):
    #     em = discord.Embed(description="aliases : `unload_cogs`, `unload_cog`, `uc`\nusage : `unload_cog <cog>`\ne.g. : `-unload_cog moderation`", color=0x2f3136)
    #     await ctx.send(embed=em)


    # @help.command()
    # async def reload_cogs(self, ctx):
    #     em = discord.Embed(description="aliases : `reload_cogs`, `reload_cog`, `rc`\nusage : `reload_cog <cog>`\ne.g. : `-reload_cog moderation`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def reload_all_cogs(self, ctx):
    #     em = discord.Embed(description="aliases : `reload_all_cogs`, `reload_all_cog`, `rac`\nusage : `reload_all_cogs`\ne.g. : `-reload_all_cogs`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    # @help.command()
    # async def setup_moderation(self, ctx):
    #     em = discord.Embed(description="aliases : `setup_moderation`, `setup`, `su`\nusage : `-setup_moderation`\ne.g. : `-setup_moderation`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # ########################################### basic related #######################################

    # @help.command()
    # async def invite(self, ctx):
    #     em = discord.Embed(description="aliases : `inv`\nusage : `invite`\ne.g. : `-invite`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def avatar(self, ctx):
    #     em = discord.Embed(description="aliases : `avatar_lookup`, `avatar`, `pfp`\nusage : `-avatar {member}|{member.id}`\ne.g. : `-pfp @.e#066 | -pfp 759090144955072522`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def member(self, ctx):
    #     em = discord.Embed(description="aliases : `member`, `lookup`, `search`\nusage : `-member {user}|{member.id}`\ne.g. : `-member @.e#066 | -member 759090144955072522`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    # @help.command()
    # async def guild(self, ctx):
    #     em = discord.Embed(description="aliases : `guild`, `server`\nusage : `-guild`\ne.g. : `-guild`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    # @help.command()
    # async def embed(self, ctx):
    #     em = discord.Embed(description="aliases : `embed`\nusage : `-embed {message}`\ne.g. : `-embed fuck you eric`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def embed_stay(self, ctx):
    #     em = discord.Embed(description="aliases : `embed_stay`\nusage : `-embed_stay {message}`\ne.g. : `-embed_stay fuck you eric`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def imbed(self, ctx):
    #     em = discord.Embed(description="aliases : `imbed`\nusage : `-imbed {image}`\ne.g. : `-imbed {image}`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    # @help.command()
    # async def imbed_stay(self, ctx):
    #     em = discord.Embed(description="aliases : `imbed_stay`\nusage : `-imbed_stay {image}`\ne.g. : `-imbed_stay {image}`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def purge(self, ctx):
    #     em = discord.Embed(description="aliases : `purge`, `clear`\nusage : `-purge {integer of messages}\ne.g. : `-purge 50`", color=0x2f3136)
    #     await ctx.send(embed=em)
    
    

    # ########################################### emoji related #######################################

    # @help.command()
    # async def steal(self, ctx):
    #     em = discord.Embed(description="aliases : `steal`, `copy`\nusage : `-steal {emoji} [*name]\ne.g. : `-steal :A_Nod_IEH: *nodding`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # ########################################### info related #######################################
        
    # @help.command()
    # async def ping(self, ctx):
    #     em = discord.Embed(description="aliases : `ping`, `\nusage : `-ping\ne.g. : `-ping`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def stats(self, ctx):
    #     em = discord.Embed(description="aliases : `stats`\nusage : `-stats\ne.g. : `-stats`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # ########################################### jail related #######################################


    # # @help.command()
    # # async def jail(self, ctx):
    # #     em = discord.Embed(description="aliases : `jail`\nusage : `-jail {user}|{member.id}\ne.g. : `-jail @.e#066 | -jail 759090144955072522`", color=0x2f3136)
    # #     await ctx.send(embed=em)

    # # @help.command()
    # # async def unjail(self, ctx):
    # #     em = discord.Embed(description="aliases : `unjail`\nusage : `-unjail {user}|{member.id}\ne.g. : `-unjail @.e#066 | -unjail 759090144955072522`", color=0x2f3136)
    # #     await ctx.send(embed=em)

    # # @help.command()
    # # async def jail_setup(self, ctx):
    # #     em = discord.Embed(description="aliases : `jail_setup`\nusage : `-jail_setup\ne.g. : `-jail_setup`", color=0x2f3136)
    # #     await ctx.send(embed=em)

    # ########################################### prefix related #######################################

    # @help.command()
    # async def prefix(self, ctx):
    #     em = discord.Embed(description="aliases : `prefix`\nusage : `-prefix\ne.g. : `-prefix`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def prefix(self, ctx):
    #     em = discord.Embed(description="aliases : `prefix change`\nusage : `-prefix change {new_prefix}\ne.g. : `-prefix !`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # ########################################### prefix related #######################################

    # @help.command()
    # async def sms(self, ctx):
    #     em = discord.Embed(description="aliases : `sms`, `send_sms`\nusage : `-sms {number} {message}\ne.g. : `-sms 6126660420 fuck you`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # @help.command()
    # async def sms(self, ctx):
    #     em = discord.Embed(description="aliases : `number`\nusage : `-number {number} \ne.g. : `-number 6126660420`", color=0x2f3136)
    #     await ctx.send(embed=em)

    # ########################################### snipe related #######################################

    # @help.command()
    # async def snipe(self, ctx):
    #     em = discord.Embed(description="aliases : `s`, `snipe`\nusage : `-s \ne.g. : `-s | -snipe`", color=0x2f3136)
    #     await ctx.send(embed=em)

async def setup(bot: commands.Bot):
    await bot.add_cog(helper(bot))
        
