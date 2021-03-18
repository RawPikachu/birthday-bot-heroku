from discord.ext import commands
from replit import db


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True
    
    async def cog_command_error(self, ctx, error):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name='setbirthday', brief="Sets your birthday.", description="You can use this command to set your birthday.")
    async def _setbirthday(self, ctx, month=None, day=None):
        if month == None or day == None:
            await ctx.send("You need to enter your birthday in this format: b!setbirthday month day")
            return
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