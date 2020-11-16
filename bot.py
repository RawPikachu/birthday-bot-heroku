import discord
from discord.ext import commands
import time

bot = commands.Bot(command_prefix='b!')

verification = {}

@bot.command()
async def setbirthday(ctx):
    user = ctx.author
    embedSetBirthday1 = discord.Embed(title="1. Please input your birthday", description="Please respond with your birthday in this format: MM/DD. Ex: 03/20. This prompt will be canceled after 5 minutes.")
    await user.send(embed=embedSetBirthday1)
    verification[f"{user.name}"] = {"step":1}
    time_start1 = time.process_time()
    while True:
        if verification[f"{user.name}"]["step"] == 2:
            break
        if time.process_time() - time_start1 == 300:
            verification.pop(f"{user.name}")
            break
    if verification[f"{user.name}"]["step"] == 2:
        raise NotImplementedError

@bot.event
async def on_message(message):
    user = message.author
    print(verification)
    if message.guild == None and message.author != bot.user:
        print(verification)
        if verification[f"{user.name}"]["step"] == 1:
            try:
                if message.strip("/")[0] <= 12 and message.strip("/")[1] <= 31:
                    verification[f"{user.name}"]["birthday"] = message
                    verification[f"{user.name}"]["step"] = 2
                    print("hello")
                else:
                    await user.send("Wrong format, please use the command b!setbirthday again.")
                    verification.pop(f"{user.name}")
            except:
                await user.send("Wrong format, please use the command b!setbirthday again.")
                verification.pop(f"{user.name}")
        else:
            print("fk you this does not wokr")
    await bot.process_commands(message)


bot.run('NzY3MTI1NjYzMzEyMTE3ODAy.X4tXcg.Qu-AgxRHGrbsNjfNY45v_uUKRw0')
print("Logged in.")