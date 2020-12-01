import subprocess
bashCommand = "pip install discord"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
import keep_alive
import os
import json
from discord.ext import tasks, commands
import discord
import datetime
from replit import db

bot = commands.Bot(command_prefix='b!')

BOTTOKEN = os.environ["BOTTOKEN"]

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
    if f"{month}/{day}" in birthdays:
        birthdays[f"{month}/{day}"].remove(userid)
    birthdays[f"{month}/{day}"].append(userid)
    db["birthdays"] = birthdays
    birthdays = db["birthdays"]
    if userid in birthdays[f"{month}/{day}"]:
        await ctx.channel.send("Your birthday has been successfully saved into the database.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

#@tasks.loop(minutes=1.0)
#async def check_for_birthday():
#    with open("birthdays.json", "r") as f:
#        birthdays = dict(json.load(f))
#        birthday_list = list(birthdays.keys())[list(birthdays.values()).index(f"{datetime.date.month}/{datetime.date.day}")]


keep_alive.keep_alive()

bot.run(BOTTOKEN)
print("Logged in.")
