from discord.ext import commands
#from discord_slash import cog_ext
#from discord_slash.context import SlashContext
#from discord_slash.model import SlashCommandOptionType
#from discord_slash.utils.manage_commands import create_option
from collections import Counter
import asyncio
import time
from db import db_adapter as db
from corkus import Corkus


class Wynncraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.server_check())
    """
    @cog_ext.cog_slash(name="findlootingworld", 
                            description="Finds the least looted wynncraft world.",
                            options=[
                                create_option(
                                    name="world",
                                    description="The Wynncraft world that you want to check. (Only the number part.)",
                                    option_type=SlashCommandOptionType.INTEGER,
                                    required=True
                                )
                            ])
    """
    async def limited(self, until):
        duration = int(round(until - time.time()))
        print('Rate limited, sleeping for {:d} seconds'.format(duration))
    
    @commands.command(name='listservers')
    async def _listservers(self, ctx):
        serverlist = db.get_server_list_all()
        for server in serverlist:
            await ctx.send(f"{server.name} {server.total_players} {server.uptime}")
            await asyncio.sleep(.25)

    @commands.command(name='findlootingworld', brief="Finds the total number of chests opened in the given wynncraft world.", description="Finds the total number of chests opened in the given wynncraft world. (Enter the world in number form)")
    async def wynncraft_findlootingworld(self, ctx, world: int):
        async with Corkus() as corkus:
            await ctx.send("Scanning server's chest count.")
            players_chests_found = {}
            players_chests_found_2 = {}
            onlineplayers = await corkus.network.online_players()
            serverlist = onlineplayers.servers
            for server in serverlist:
                if server.name == f"WC{world}":
                    chosen_server = server
                    break
                else:
                    await ctx.send("Enter a valid server :/")
            for i in range(2):
                if i == 1:
                    await ctx.send("Starting second scan.")
                partial_players = chosen_server.players
                for partial_player in partial_players:
                    player = await partial_player.fetch()
                    player_chests_found = player.statistics.chests_found
                    if i == 0:
                        players_chests_found[player.username] = player_chests_found
                    else:
                        players_chests_found_2[player.username] = player_chests_found
                if i == 1:
                    server_still_exists = False
                    onlineplayers = await corkus.network.online_players()
                    serverlist = onlineplayers.servers
                    for server in serverlist:
                        if server.name == f"WC{world}":
                            server_still_exists = True
                            break
                    if not server_still_exists:
                        await ctx.send("Your server probably shutdown.")
                        return
                            
                if i == 0:
                    await ctx.send("Scanning probably completed, wait 10 minutes for second scan.")
                    await asyncio.sleep(600)

            keys_to_delete = [key for key in players_chests_found_2 if not (key in players_chests_found)]
            
            for key in keys_to_delete:
                del players_chests_found_2[key]
            
            keys_to_delete = [key for key in players_chests_found if not (key in players_chests_found_2)]
            
            for key in keys_to_delete:
                del players_chests_found[key]
            
            c_players_chests_opened_2 = Counter(players_chests_found_2)
            c_players_chests_opened = Counter(players_chests_found)
            chests_opened_timeframe = c_players_chests_opened_2 - c_players_chests_opened

            chests_opened_list = chests_opened_timeframe.values()
            total_chests_opened = sum(chests_opened_list)
            await ctx.send(f"{ctx.author.mention} {total_chests_opened} chests have been opened in the past 10 minutes.")
    
    async def server_check(self):
        async with Corkus() as corkus:
            while True:
                onlineplayers = await corkus.network.online_players()
                serverlist = onlineplayers.servers
                
                db_server_list = db.get_server_list_all()

                servernamelist = [server.name for server in serverlist]

                db_server_name_list = [db_server.name for db_server in db_server_list]

                for db_server_name in db_server_name_list:
                    if not (db_server_name in servernamelist):
                        db.delete_server_list(db_server_name)
                
                for servername in servernamelist:
                    if not (servername in db_server_name_list):
                        for server in serverlist:
                            if server.name == servername:                           
                                db.create_server_list(servername, server.total_players, int(time.time()))
                
                db_server_list = db.get_server_list_all()
                
                for db_server in db_server_list:
                    db_server.calculate_uptime()
                    await db_server.update_total_players()
                    db.update_server_list(db_server.name, db_server.total_players, db_server.timestamp, uptime=db_server.uptime)

                await asyncio.sleep(30)
            
            