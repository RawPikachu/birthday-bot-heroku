from discord.ext.commands import bot
from discord.player import FFmpegPCMAudio
from discord.utils import get
import keep_alive
import os
from discord.ext import commands
import discord
from datetime import datetime
from replit import db
from pytz import timezone
import asyncio


class BirthdayBot(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True
    
    async def cog_command_error(self, ctx, error):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name='setbirthday')
    async def _setbirthday(self, ctx, month, day):
        user = ctx.author
        userid = str(user.id)
        try:
            month, day = int(month), int(day)
        except:
            await ctx.channel.send("Please enter month and day without brackets and enter it in its number form.")
            return
        if month > 12 or month < 1 or day > 31 or day < 1:
            await ctx.channel.send("Please enter a valid date.")
            return
        if month % 2 == 0 and day > 30:
            await ctx.channel.send("Please enter a valid date.")
            return
        if month == 2 and day > 29:
            await ctx.channel.send("Please enter a valid date.")
            return
        birthdays = db["birthdays"]
        if any(userid in val for val in birthdays.values()):
            keys = [key for key, value in birthdays.items() if userid in value]
            key = keys[0]
            birthdays[key].remove(userid)
            if birthdays[key] == []:
                del birthdays[key]
        if not(f"{month}/{day}" in birthdays):
            birthdays[f"{month}/{day}"] = []
        birthdays[f"{month}/{day}"].append(userid)
        db["birthdays"] = birthdays
        birthdays = db["birthdays"]
        if userid in birthdays[f"{month}/{day}"]:
            await ctx.channel.send("Your birthday has been successfully saved into the database.")

    @commands.command(name='join', invoke_without_subcommand=True)
    @commands.has_role("DJ")
    async def _join(self, ctx):
        if ctx.author.voice:
            destination = ctx.author.voice.channel
            await destination.connect()
            await ctx.send("Bot joined.")
        else:
            await ctx.send("You must be in a voice channel first.")

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_role("DJ")
    async def _leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Bot left.")
        else:
            await ctx.send('Not connected to any voice channel.')

    @commands.command(name="play")
    @commands.has_role("DJ")
    async def _play(self, ctx, link):
        if not ctx.voice_client:
            await ctx.invoke(self._join)
        source = FFmpegPCMAudio(link)
        ctx.voice_client.play(source)
        await ctx.send("Playing audio track.")



intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='b!', intents=intents)
bot.add_cog(BirthdayBot(bot))
tz = timezone("US/Eastern")

@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))

async def check_for_birthday():
    while True:
        now = datetime.now(tz)
        birthdays = db["birthdays"]
        if f"{now.month}/{now.day}" in birthdays:
            if now.hour == 8 and now.minute == 30:
                for guild in self.bot.guilds:
                    users_to_celebrate = []
                    for user_to_celebrate in birthdays[f"{now.month}/{now.day}"]:
                        if guild.get_member(int(user_to_celebrate)) is not None:
                            users_to_celebrate.append(user_to_celebrate)
                    if discord.utils.get(guild.text_channels, name="annoncement") == None:
                        await guild.create_text_channel('annoncement')
                    channel = discord.utils.get(guild.channels, name="annoncement")
                    await channel.send("@everyone Hey guys! Today is a special day, it's the birthday of the following user(s)! : {}. Happy birthday!".format(" ".join([f"<@{int(user)}>" for user in users_to_celebrate])))
        if now.month == 12 and now.day == 25 and now.hour == 8 and now.minute == 30:
            for guild in self.bot.guilds:
                if discord.utils.get(guild.text_channels, name="annoncement") == None:
                    await guild.create_text_channel('annoncement')
                channel = discord.utils.get(guild.channels, name="annoncement")
                await channel.send("Merry Christmas @everyone ! Go spend time with your family! :>")
        await asyncio.sleep(60)

BOTTOKEN = os.environ["BOTTOKEN"]

keep_alive.keep_alive()

bot.loop.create_task(check_for_birthday())
bot.run(BOTTOKEN)
