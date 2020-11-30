import subprocess
bashCommand = "pip install discord"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
bashCommand = "pip install multipledispatch"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
import keep_alive
import os
import json
from discord.ext import commands
import discord
from multipledispatch import dispatch
bot = commands.Bot(command_prefix='b!')

BOTTOKEN = os.environ["BOTTOKEN"]

@dispatch(commands.Context(), str, str)
@bot.command()
async def setbirthday(ctx, month, day):
    user = ctx.author
    userid = str(user.id)
    try:
        month, day = int(month), int(day)
    except:
        await ctx.channel.send("Please enter month and day without brackets and enter it in its number form.")
        return
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

@dispatch(commands.Context())
@bot.command()
async def setbirthday(ctx):
    await ctx.channel.send("Usage: b!setbirthday month day")

@dispatch(commands.Context(), str)
@bot.command()
async def setbirthday(ctx, _):
    await ctx.channel.send("Usage: b!setbirthday month day")


@bot.event
async def on_message(message):
    await bot.process_commands(message)

keep_alive.keep_alive()

bot.run(BOTTOKEN)
print("Logged in.")
