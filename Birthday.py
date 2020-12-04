import subprocess
bashCommand = "pip install discord pytz"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
import keep_alive
import os
from discord.ext import commands
import discord
from datetime import datetime
from replit import db
from pytz import timezone
import asyncio

bot = commands.Bot(command_prefix='b!')

BOTTOKEN = os.environ["BOTTOKEN"]

tz = timezone("US/Eastern")

@bot.command()
async def setbirthday(ctx, month, day):
    user = ctx.author
    userid = str(user.id)
    try:
        month, day = int(month), int(day)
    except:
        await ctx.channel.send("Please enter month and day without brackets and enter it in its number form.")
        return
    if month > 12 or day > 31:
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

@bot.event
async def on_message(message):
    await bot.process_commands(message)

async def check_for_birthday():
    while True:
        now = datetime.now(tz)
        birthdays = db["birthdays"]
        print(1)
        if f"{now.month}/{now.day}" in birthdays:
            print(2)
            if now.hour == 8 and now.minute == 30:
                print(3)
                for guild in bot.guilds():
                    users_to_celebrate = []
                    for user_to_celebrate in birthdays[f"{now.month}/{now.day}"]:
                        if guild.get_member(int(user_to_celebrate)) is not None:
                            users_to_celebrate.append(user_to_celebrate)
                    if discord.utils.get(guild.text_channels, name="annoncements") == None:
                        await guild.create_text_channel('annoncements')
                    channel = discord.utils.get(guild.channels, name="annoncements")
                    await channel.send("@everyone Hey guys! Today is a special day, it's the birthday of the following users! : {}".format(" ".join([f"<@{int(user)}>" for user in users_to_celebrate])))
        await asyncio.sleep(60)
                

keep_alive.keep_alive()

bot.loop.create_task(check_for_birthday())

bot.run(BOTTOKEN)
print("Logged in.")
