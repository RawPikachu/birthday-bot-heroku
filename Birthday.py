bashCommand = "pip install discord"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

import discord
from discord.ext import commands
import json
import os
import keep_alive

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
    with open("birthdays.json", "r") as f:
        birthdays = dict(json.load(f))
    if userid in birthdays:
        del birthdays[userid]
    birthdays[userid] = "{}/{}".format(month, day)
    with open("birthdays.json", "w") as f:
        json.dump(birthdays, f)
    with open("birthdays.json", "r") as f:
        birthdays = dict(json.load(f))
    if userid in birthdays:
        await ctx.channel.send("Your birthday has been successfully saved into the database.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)                      

keep_alive.keep_alive()

bot.run(BOTTOKEN)
print("Logged in.")