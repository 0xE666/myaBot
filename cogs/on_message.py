import discord, time, sys, os, asyncio, requests, traceback
from discord.ext import commands
from discord.utils import get
from discord import Embed, File, DMChannel
from yt_dlp import YoutubeDL
from discord import File
from asyncio import sleep
import subprocess, os, re, pytube
from numerize import numerize

# get parent directory to import relative modules
sys.path.insert(0, str(os.getcwd()))
from datetime import datetime
from utils import utility
from db import db
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class loggerOutputs:
    def error(msg):
        pass
    def warning(msg):
        pass
    def debug(msg):
        pass


class on_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = utility.utility_api()
        self.db = db.database_manager()

    def timestamp(self):
        return time.strftime("%H:%M:%S")

    def get_tiktok_data(self, url):
        requests.adapters.DEFAULT_RETRIES = 10

        data = {
            "url": f"{url}",
            "hd": 1
        }
            
        try:
            s = requests.Session()
            s.keep_alive = False
            req = s.post("https://www.tikwm.com/api/", data=data, timeout=(2, 5), verify=False)
            json_data = req.json()
        except:
            s = requests.Session()
            s.keep_alive = False
            req = s.post("https://www.tikwm.com/api/", data=data, timeout=(2, 5), verify=False)
            json_data = req.json()

        return json_data

    def get_parsed_data(self, url):

        json_data = self.get_tiktok_data(url)
        
        tiktok_data = json_data["data"]
        tiktok_author_data = tiktok_data["author"]


        tiktok_id = tiktok_data.get("id", False)
        tiktok_title = tiktok_data.get("title", False)
        tiktok_video = tiktok_data.get("play", False)
        tiktok_views = tiktok_data.get("play_count", False)
        tiktok_likes = tiktok_data.get("digg_count", False)
        tiktok_comments = tiktok_data.get("comment_count", False)
        tiktok_shares = tiktok_data.get("share_count", False)
        tiktok_created = tiktok_data.get("create_time", False)
        tiktok_username = tiktok_author_data.get("unique_id", False)
        tiktok_profile_picture = tiktok_author_data.get("avatar", False)

        tiktok_data = {
            "creator_username": f"{tiktok_username}",
            "video_id": f"{tiktok_id}",
            "video_title": f"{tiktok_title}",
            "video_views": f"{tiktok_views}",
            "video_likes": f"{tiktok_likes}",
            "video_comments": f"{tiktok_comments}",
            "video_shares": f"{tiktok_shares}",
            "video_create": f"{tiktok_created}",
            "video_url": f"{tiktok_video}",
            "creator_pfp_url": f"{tiktok_profile_picture}"
        }

        return tiktok_data

    def generate_uwu(self, input_text):
        length = len(input_text)
        
        output_text = ''
        
        for i in range(length):
            
            current_char = input_text[i]
            previous_char = '&# 092;&# 048;'
            
            if i > 0:
                previous_char = input_text[i - 1]
            
            if current_char == 'L' or current_char == 'R':
                output_text += 'W'
            
            elif current_char == 'l' or current_char == 'r':
                output_text += 'w'

            elif current_char == 'h' or current_char == "H":
                output_text += 'h-h'
            
            elif current_char == 'O' or current_char == 'o':
                if previous_char == 'N' or previous_char == 'n' or previous_char == 'M' or previous_char == 'm':
                    output_text += "yo"
                else:
                    output_text += current_char
            else:
                output_text += current_char
    
        return output_text


    @commands.Cog.listener()
    async def on_message(self, message):

        msg_id = message.id
        mess_author_id = message.author.id
        channel = message.channel.id

        if self.utility.check_uwu_locked(mess_author_id):
            msg_channel = self.bot.get_channel(channel)
            msg = await msg_channel.fetch_message(msg_id)
            await msg.delete()

            webhook = await msg_channel.create_webhook(name=message.author.name)
            await webhook.send(str(self.generate_uwu(message.content)), avatar_url=message.author.avatar.url)
            
            webhooks = await msg_channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
        
            # mess_author = f"{message.author.display_name}#{message.author.discriminator}"
            # mess_author_id = message.author.id
            # mess = message.content
            # print(f"[{mess_author_id}]: {mess_author} - {mess}")



        requests.adapters.DEFAULT_RETRIES = 10
        if "tiktok" in message.content:
            valid = re.findall("tiktok.com.{1,30}/\d{19,19}|vt.tiktok.com/[a-zA-Z0-9]{5,12}/|tiktok.com/.{10,25}=\d{19,}", message.content)
            if valid:
                
                try:
                    os.remove("data/videos/tomb_tikok45345341.mp4")
                except:
                    pass

                url = message.content
                msg_id = message.id
                channel = message.channel.id
                msg_channel = self.bot.get_channel(channel)
                msg1 = await msg_channel.fetch_message(msg_id)
                await msg1.delete()

                parsed = self.get_parsed_data(url)


                embed1 = Embed(description=f"\nattempting to download...", color=0x2f3136, timestamp=datetime.utcnow())
                embed1.set_footer(text=f"{message.author.display_name}#{message.author.discriminator}",  icon_url=message.author.display_avatar)
                msg = await msg_channel.send(embed=embed1, delete_after=1.5)

                try:
                    s = requests.session()
                    s.keep_alive = False
                    resp = s.get(parsed["video_url"], timeout=(2,5), verify=False)
                    with open("data/videos/tomb_tikok45345341.mp4", "wb") as f:
                        f.write(resp.content)

                except TypeError:
                    s = requests.session()
                    s.keep_alive = False
                    resp = s.get(parsed["video_url"], timeout=(2,5), verify=False)
                    with open("data/videos/tomb_tikok45345341.mp4", "wb") as f:
                        f.write(resp.content)


                embed = discord.Embed(color=0x2f3136)
                file = discord.File("data/videos/tomb_tikok45345341.mp4", filename="tomb_tikok45345341.mp4")
                embed.set_image(url="attachment://tomb_tikok45345341.mp4")
                await msg_channel.send(file=file)


                embed1 = Embed(description=f"[TikTok]({url}) requested by {message.author.mention}", color=0x2f3136)
                embed1.set_author(name=f"{parsed['creator_username']}", icon_url=parsed["creator_pfp_url"])

                timestamp = int(parsed["video_create"])
                value = datetime.fromtimestamp(timestamp)
                parsed_ts = value.strftime('%m/%d/%Y %I:%M %p')

                embed1.set_footer(text=f"❤️ {numerize.numerize(int(parsed['video_likes']))}  👀 {numerize.numerize(int(parsed['video_views']))}  💬 {numerize.numerize(int(parsed['video_comments']))}  ⛤  {parsed_ts}", icon_url="https://cdn.discordapp.com/attachments/1030212403687854230/1043981794850115584/emote.png")
                msg = await msg_channel.send(embed=embed1)


                return os.remove("data/videos/tomb_tikok45345341.mp4")


        # if "youtube" in message.content:
        #     valid_url = re.findall(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", message.content)
        #     if valid_url:
        #         try:
        #             os.remove("data/videos/tomb_yt4534555.mp4")
        #         except:
        #             pass

        #         url = message.content
        #         msg_id = message.id
        #         channel = message.channel.id

        #         msg_channel = self.bot.get_channel(channel)
        #         msg1 = await msg_channel.fetch_message(msg_id)
        #         await msg1.delete()

        #         download_embed = Embed(description=f"\nattempting to download...", color=0x2f3136, timestamp=datetime.utcnow())
        #         download_embed.set_footer(text=f"{message.author.display_name}#{message.author.discriminator}",  icon_url=message.author.display_avatar)
        #         await msg_channel.send(embed=download_embed, delete_after=1.5)

        #         video = pytube.YouTube(url)
        #         video_title = video.title
        #         video_views = video.views
        #         author = video.author
        #         author_url = video.channel_url
        #         creation_date = video.publish_date
        #         video_length = video.length
        #         if video_length >= 720:
        #             video.streams.get_by_resolution("360p").download("data/videos", filename="tomb_yt4534555.mp4")
        #         else:
        #             video.streams.get_by_resolution("720p").download("data/videos", filename="tomb_yt4534555.mp4")


        #         file = discord.File("data/videos/tomb_yt4534555.mp4", filename="tomb_yt4534555.mp4")
        #         await msg_channel.send(file=file)

        #         video_embed = Embed(description=f"[YouTube]({url}) requested by {message.author.mention}\n{video_title}", color=0x2f3136)
        #         video_embed.set_author(name=f"{author}", icon_url="https://cdn.discordapp.com/attachments/1042656075209511002/1044328416897417246/unknown.png", url=author_url)

        #         creation_date_parsed = str(creation_date).split(" ")[0]
        #         date_obj = datetime.strptime(creation_date_parsed, "%Y-%m-%d")
        #         date = date_obj.strftime("%b %d, %Y")

        #         video_embed.set_footer(text=f"👀 {numerize.numerize(int(video_views))}  ⛤  {date}", icon_url="https://cdn.discordapp.com/attachments/1030212403687854230/1043981794850115584/emote.png")
        #         await msg_channel.send(embed=video_embed)

                
    

async def setup(bot: commands.Bot):
    await bot.add_cog(on_message(bot))