from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from replit import db


class Music(commands.Cog):    
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')
        return True
    
    async def cog_command_error(self, ctx, error):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True, brief="The bot joins your voice channel.", description="This command makes the bot join your voice channel.")
    @commands.has_role("DJ")
    async def _join(self, ctx):
        if ctx.author.voice:
            destination = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(destination)
                await ctx.send("Bot joined.")
            else:
                await destination.connect()
                await ctx.send("Bot joined.")
        else:
            await ctx.send("You must be in a voice channel first.")

    @commands.command(name='leave', aliases=['disconnect', "stop"], brief="The bot leaves your voice channel.", description="This command makes the bot leave your voice channel.")
    @commands.has_role("DJ")
    async def _leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Bot left.")
        else:
            await ctx.send('Not connected to any voice channel.')

    @commands.command(name="play", brief="Joins your voice channel and plays the audio/video from the provided url.", description="This command makes the bot join your voice channel if you are not already in one and plays the audio/video from the provided url. (The url must end in an audio/video extension.)")
    @commands.has_role("DJ")
    async def _play(self, ctx, url=None):
        if url == None:
            await ctx.send('You must provide a link providing an audio or video track.')
        else:
            await ctx.invoke(self._join)
            source = FFmpegPCMAudio(url)
            ctx.voice_client.play(source)
            ctx.voice_client.source = PCMVolumeTransformer(ctx.voice_client.source, db["volume"][ctx.guild.id])
            await ctx.send("Playing audio track.")

    @commands.command(name="setservervolume", aliases=['setvolume', 'servervolume', 'volume'], brief="Sets the volume for the server.", description="This commands allows you to set the volume of audios being played in the server.")
    @commands.has_permissions(administrator=True)
    async def _setservervolume(self, ctx, volume=None):
        volume = int(volume)
        if volume == None or volume < 0 or volume > 100:
            await ctx.send("You have to provide a volume between 0 and 100")
        db["volume"][ctx.guild.id] = volume/100