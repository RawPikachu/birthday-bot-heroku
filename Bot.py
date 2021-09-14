import discord
from discord.ext import commands
from Music import Music
from Birthday import Birthday
from General import General
from ErrorHandler import CommandErrorHandler
from Wynncraft import Wynncraft
import asyncio
import os



intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='b!', intents=intents, help_command=None)
bot.add_cog(Music(bot))
bot.add_cog(Birthday(bot))
bot.add_cog(General(bot))
bot.add_cog(Wynncraft(bot))
bot.add_cog(CommandErrorHandler(bot))
temp_disabled_command = bot.get_command("volume")
temp_disabled_command.enabled = False

@bot.event
async def on_ready():
    print("Logged in as:\n{0.user.name}\n{0.user.id}".format(bot))

async def rate_limit_check():
    import requests

    r = requests.head(url="https://discord.com/api/v1")
    try:
        print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
    except:
        print("No rate limit")
    asyncio.sleep(3600)

BOTTOKEN = os.environ["BOTTOKEN"]

bot.loop.create_task(rate_limit_check())
bot.run(BOTTOKEN)
