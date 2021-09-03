from discord.ext import commands
import discord
from Help import MyHelpCommand
import inspect
import db.db_adapter as db


class General(commands.Cog, commands.MinimalHelpCommand):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelpCommand()
        self.bot.help_command.cog = self

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True
    
    @commands.command(name="ping", brief="Displays the bot's ping.", description="This command allows you to display the bot's ping.")
    async def _ping(self, ctx):
        if round(self.bot.latency * 1000) <= 50:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x44ff44)
        elif round(self.bot.latency * 1000) <= 100:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xffd000)
        elif round(self.bot.latency * 1000) <= 200:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0xff6600)
        else:
            embed=discord.Embed(title="PING", description=f":ping_pong: Pong! The ping is **{round(self.bot.latency *1000)}** milliseconds!", color=0x990000)
        await ctx.send(embed=embed)
    
    @commands.command(name='eval', brief="Runs an actual command.", description="This command allows you to run an actual command in python.")
    @commands.is_owner()
    async def _eval(self, ctx, *, command):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'db': db
        }
        env.update(globals())
        
        res2 = eval(command, env)
        if inspect.isawaitable(res2):
            embed = discord.Embed(
            title='Eval', description='' , colour=discord.Colour.green())

            embed.add_field(name='Input', value=f'||{await res2}||', inline=False)


            await ctx.send(embed=embed)
    
    