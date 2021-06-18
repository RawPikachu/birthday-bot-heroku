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

    @commands.command(name='join', invoke_without_subcommand=True, brief="The bot joins your voice channel.", description="This command makes the bot join your voice channel.")
    @commands.check_any(commands.is_owner(), commands.has_role("DJ"))
    async def _join(self, ctx):
        if ctx.author.voice:
            destination = ctx.author.voice.channel
            if ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
                await ctx.send("Bot is already connected.")
            elif ctx.voice_client:
                await ctx.voice_client.move_to(destination)
                if ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
                    await ctx.send("Bot moved to your channel.")
                else:
                    await ctx.send("Bot was unable to move to your channel.")
            else:
                await destination.connect()
                if ctx.voice_client:
                    await ctx.send("Bot joined.")
                else:
                    await ctx.send("Bot was unable to join your channel.")
        else:
            await ctx.send("You must be in a voice channel first.")

    @commands.command(name='leave', aliases=['disconnect', "stop"], brief="The bot leaves your voice channel.", description="This command makes the bot leave your voice channel.")
    @commands.check_any(commands.is_owner(), commands.has_role("DJ"))
    async def _leave(self, ctx):
        if ctx.voice_client and not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("You have to be in the same channel as the bot to use this command.")
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            if not ctx.voice_client:
                await ctx.send("Bot left.")
            else:
                await ctx.send("Bot was unable to leave the channel.")
        else:
            await ctx.send('Not connected to any voice channel.')

    @commands.command(name="play", brief="Joins your voice channel and plays the audio/video from the provided url.", description="This command makes the bot join your voice channel if you are not already in one and plays the audio/video from the provided url. (The url must end in an audio/video extension.)")
    @commands.check_any(commands.is_owner(), commands.has_role("DJ"))
    async def _play(self, ctx, url=None):
        if url == None:
            await ctx.send('You must provide a link providing an audio or video track.')
        else:
            db_volume = db["volume"]
            if not str(ctx.guild.id) in db_volume:
                db_volume[str(ctx.guild.id)] = 1
                db["volume"] = db_volume
            if (ctx.voice_client and not ctx.author.voice.channel == ctx.voice_client.channel) or (not ctx.voice_client):
                await ctx.invoke(self._join)
            source = FFmpegPCMAudio(url)
            ctx.voice_client.play(source)
            ctx.voice_client.source = PCMVolumeTransformer(ctx.voice_client.source, db["volume"][str(ctx.guild.id)])
            if ctx.voice_client:
                await ctx.send("Playing audio track.")
            else:
                await ctx.send("Failed to play audio track.")

    @commands.command(name="setservervolume", aliases=['setvolume', 'servervolume', 'volume'], brief="Sets the volume for the server.", description="This commands allows you to set the volume of audios being played in the server.")
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def _setservervolume(self, ctx, volume=None):
        volume = float(volume)
        if volume == None or volume < 0 or volume > 100:
            await ctx.send("You have to provide a volume between 0 and 100")
            return
        db_volume = db["volume"]
        if str(ctx.guild.id) in db_volume:       
            del db_volume[str(ctx.guild.id)]
        db_volume[str(ctx.guild.id)] = volume/100
        db["volume"] = db_volume
        await ctx.send(f"Volume is set to {volume}%.")

    @commands.command(name="random", brief="*cough* Plays a random song.", description="*ahem* This commands allows you to play a random song in your voice channel.")
    @commands.check_any(commands.is_owner(), commands.has_role("DJ"))
    async def _random(self, ctx):
        await ctx.invoke(self._play, ctx, url="https://cdn.discordapp.com/attachments/767132531350700062/855454319411068928/Never_Gonna_Give_You_Up_Original.mp3")
        if ctx.voice_client:
            await ctx.send("haha jk.")