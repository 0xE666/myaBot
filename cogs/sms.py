from ast import Delete
from unicodedata import category
import discord, time
from discord.ext import commands
from typing import Union, Any, Callable, Tuple, List, Coroutine, Optional
import sys, os, asyncio, requests, humanfriendly, telnyx, requests, re
from datetime import datetime, timedelta

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from utils import utility
from datetime import datetime

requests.adapters.DEFAULT_RETRIES = 5

def timestamp():
    return time.strftime('%H:%M:%S')

class sms_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.utility = utility.utility_api()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[cog-ready]: {__class__.__name__}')
    
    @commands.has_permissions(manage_messages=True)
    @commands.command(name='sms', aliases=['send_sms'], description='text a number', help='{prefix}sms|send_sms [number] [message]\n')
    async def sms_command(self, ctx: commands.Context, number: int, *, text):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        try:
            if ctx.author.bot:
                return
            
            if self.utility.check_white_listed(ctx.author.id):

                try:
                    telnyx.Message.create(
                        api_key="",
                        from_="+15804031129",
                        to=f"+1{number}",
                        text=text,
                        messaging_profile_id="40017cf0-6600-40b4-95ec-def2618cf696"
                    )

                except (commands.MissingRequiredArgument) as e:
                    embed = self.utility.format_error(ctx.author, e)
                    return await ctx.send(embed=embed)
                except Exception as e:
                    embed = self.utility.format_error(ctx.author, e)
                    return await ctx.send(embed=embed)


                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'sms sent',
                    color=discord.Color.green()
                )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.",delete_after=5)

        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)
    
    def search_number(self, number):
        requests.adapters.DEFAULT_RETRIES = 10

        api_key = ""

        valid_number = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", str(number))
        if valid_number:
            url = f"https://api.telnyx.com/v2/number_lookup/+1{valid_number[0]}?type=caller-name"
            headers = {
                "content-type": "application/json",
                "accept": "application/json",
                "Authorization": f"Bearer {api_key}",
            }

            r = requests.get(url, headers=headers)
            caller_name = r.json()['data']['caller_name']
            caller_name = caller_name.get("caller_name", "unknown")
            phone_format = r.json()['data']['national_format']
            city = r.json()['data']['portability']['city']
            state = r.json()['data']['portability']['state']

            data = {
                "name": f"{caller_name}",
                "format": f"{phone_format}",
                "location": f"{city}, {state}"
            }

            return data

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='number', aliases=['number_search'], description='search a number', help='{prefix}number|number_search [number]\n')
    async def number_search_command(self, ctx: commands.Context, number):
        await asyncio.sleep(1)
        await ctx.message.delete()
        async with ctx.typing():
            await asyncio.sleep(0.5)
        try:
            if ctx.author.bot:
                return
            
            if self.utility.check_white_listed(ctx.author.id):
                if len(number) > 10:
                    return await ctx.send(f"{ctx.author.mention}, number must be no more than 10 digits.",delete_after=5)
                data = self.search_number(number)
                embed = self.utility.create_embed(
                    ctx.author,
                    title='success',
                    description=f'successfully searched',
                    color=discord.Color.green()
                    )

                embed.add_field(
                    name=f"`{data['format']}`",
                    value=f"`{data['name']}\n{data['location']}`"
                )

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{ctx.author.mention}, you are not whitelisted contact server owner.", delete_after=5)

        except Exception as e:
            embed = self.utility.format_error(ctx.author, e)
            return await ctx.send(embed=embed, delete_after=90)

async def setup(bot: commands.Bot):
    await bot.add_cog(sms_cog(bot))
