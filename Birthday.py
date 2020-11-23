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
    with open("birthdays.json", "r") as f:
        birthdays = dict(json.load(f))
    if birthdays.has_key(userid):
        del birthdays[userid]
    birthdays[userid] = "{}/{}".format(month, day)
    with open("birthdays.json", "w") as f:
        json.dump(f)
    with open("birthdays.json", "r") as f:
        birthdays = dict(json.load(f))
    if birthdays.has_key(userid):
        await ctx.channel.send("Your birthday has been successfully saved into the database.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)                      

keep_alive.keep_alive()

bot.run(BOTTOKEN)
print("Logged in.")