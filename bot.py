import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix='b!')

BOTTOKEN = os.environ("BOTTOKEN")

@bot.command()
async def setbirthday(ctx, month, day):
    user = ctx.author
    userid = str(user.id)
    with open("birthdays.json", "r") as f:
        birthdays = dict(json.load(f))
    if birthdays.has_key(userid):
        del birthdays[userid]
    birthdays[userid] = "{}/{}".format(month, day)
    with open("birthdays.json", "w"):
        json.dump()

            
            


bot.run(BOTTOKEN)
print("Logged in.")