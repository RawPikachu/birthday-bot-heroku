from discord.player import FFmpegPCMAudio
import keep_alive
import os
from discord.ext import commands
import discord
from datetime import datetime
from replit import db
from pytz import timezone
import asyncio

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='b!', intents=intents)
voice_states = []

BOTTOKEN = os.environ["BOTTOKEN"]

tz = timezone("US/Eastern")

def get_voice_state(ctx):
    state = voice_states.get(ctx.guild.id)
    if not state:
        state = discord.VoiceState
        voice_states[ctx.guild.id] = state
    return state

def cog_unload(self):
    for state in self.voice_states.values():
        self.bot.loop.create_task(state.stop())

def cog_check(self, ctx: commands.Context):
    if not ctx.guild:
        raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
    return True

async def cog_before_invoke(ctx):
    voice_state = get_voice_state()

@bot.command()
async def setbirthday(ctx, month, day):
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

@bot.command()
@bot.command.has_role("DJ")
async def join(ctx):
    destination = ctx.author.voice.channel
    if ctx.voice_state.voice:
        await ctx.voice_state.voice.move_to(destination)
        return
    ctx.voice_state.voice = await destination.connect()

@bot.command()
@bot.command.has_role("DJ")
async def leave(ctx):
    if not ctx.voice_state.voice:
        return await ctx.send('Not connected to any voice channel.')
    
    await ctx.voice_state.stop()

@bot.command()
@bot.command.has_role("DJ")
async def play(ctx, link):
    if not ctx.voice_state.voice:
        await ctx.invoke(join)
    source = FFmpegPCMAudio(link)
    ctx.voice_client.play(source)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@join.before_invoke
@play.before_invoke
async def ensure_voice_state(ctx):
    if not ctx.author.voice or not ctx.author.voice.channel:
        raise commands.CommandError('You are not connected to any voice channel.')

    if ctx.voice_client:
        if ctx.voice_client.channel != ctx.author.voice.channel:
            raise commands.CommandError('Bot is already in a voice channel.')

async def check_for_birthday():
    await bot.wait_until_ready()
    while True:
        now = datetime.now(tz)
        birthdays = db["birthdays"]
        if f"{now.month}/{now.day}" in birthdays:
            if now.hour == 8 and now.minute == 30:
                for guild in bot.guilds:
                    users_to_celebrate = []
                    for user_to_celebrate in birthdays[f"{now.month}/{now.day}"]:
                        if guild.get_member(int(user_to_celebrate)) is not None:
                            users_to_celebrate.append(user_to_celebrate)
                    if discord.utils.get(guild.text_channels, name="annoncement") == None:
                        await guild.create_text_channel('annoncement')
                    channel = discord.utils.get(guild.channels, name="annoncement")
                    await channel.send("@everyone Hey guys! Today is a special day, it's the birthday of the following user(s)! : {}. Happy birthday!".format(" ".join([f"<@{int(user)}>" for user in users_to_celebrate])))
        if now.month == 12 and now.day == 25 and now.hour == 8 and now.minute == 30:
            for guild in bot.guilds:
                if discord.utils.get(guild.text_channels, name="annoncement") == None:
                    await guild.create_text_channel('annoncement')
                channel = discord.utils.get(guild.channels, name="annoncement")
                await channel.send("Merry Christmas @everyone ! Go spend time with your family! :>")
        await asyncio.sleep(60)
                

keep_alive.keep_alive()

bot.loop.create_task(check_for_birthday())

bot.run(BOTTOKEN)
print("Logged in.")
