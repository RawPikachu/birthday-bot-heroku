from discord.ext import commands
from discord import utils
from datetime import datetime, timedelta
import asyncio
import db.db_adapter as database


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.today = (datetime.today() - timedelta(days=1)).date()
        self.bot.loop.create_task(self.birthday_loop())

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True

    @commands.command(name='setbirthday', brief="Sets your birthday.", description="You can use this command to set your birthday.")
    async def _setbirthday(self, ctx, month=None, day=None, year=-1):
        if month == None or day == None:
            await ctx.send("You need to enter your birthday in this format: b!setbirthday month day year (Please do note that year is optional)")
            return
        user = ctx.author
        if user.bot:
            return
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
        database.create_birthday(user_id=user.id, day=day, month=month, year=year)
        birthday = database.get_birthday_one(user_id=user.id)
        if birthday:
            await ctx.send(f"Successfully saved your birthday ({birthday.month}/{birthday.year}")
        
    async def birthday_loop(self):
        while not self.bot.is_closed:
            await asyncio.sleep(3600)
            if datetime.today().date() != self.today:
                self.today = datetime.today().date()
                for guild in self.bot.guilds:
                    birthdays = birthdays_today_guild(guild)
                    if len(birthdays) != 0:
                        if utils.get(guild.text_channels, name="birthdays") == None:
                            await guild.create_text_channel('birthdays')
                        channel = utils.get(guild.channels, name="birthdays")
                        jump = ''
                        message = '@ everyone\n'
                        for bd in birthdays:
                            member = utils.get(guild.members, id=bd.user_id)
                            message = f'{jump} {member.mention}, Happy birthday!'
                            jump = '\n'
                        await channel.send(message)
                        break

def birthdays_today_guild(guild):
    birthdays = []
    today = datetime.today().date()
    for member in guild.members:
        if member.bot:
            continue
        birthday = database.get_birthday_one(user_id=member.id)
        if birthday is not None:
            if today.day == birthday.day and today.month == birthday.month:
                birthdays.append(birthday)
    return birthdays