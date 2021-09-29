from discord.ext import commands
import discord


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(title="Commands List", color=discord.Color.gold(), description='')
        e.set_author(name="Birthday Bot", icon_url="https://cdn.discordapp.com/avatars/767125663312117802/c1109ff318c462a0229cf814e9c85139.png?size=128")
        e.set_footer(text="No more status page lul.")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)
