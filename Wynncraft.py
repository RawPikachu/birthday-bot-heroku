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
from tabulate import tabulate
import json


class Wynncraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.server_check())
        self.bot.loop.create_task(self.chest_count_check())
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
        db_server_list = db.get_server_list_all()
        table = [[db_server.name, db_server.total_players, db_server.uptime, db_server.min30_chest_count] for db_server in db_server_list]
        table.insert(0, ["Server", "Player Count", "Uptime (min)", "Chest Count (30 mins)"])
        tabulated_table = tabulate(table)
        await ctx.send(f"```prolog\n{tabulated_table}\n```")

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
                                db.create_server_list(servername, server.total_players, int(time.time()), min30_chest_count=None, chest_count=None, last_chest_count=None)
                
                db_server_list = db.get_server_list_all()

                onlineplayers = await corkus.network.online_players()
                serverlist = onlineplayers.servers
                
                for db_server in db_server_list:
                    db_server.calculate_uptime()
                    for server in serverlist:
                        if server.name == db_server.name:
                            db_server.total_players = server.total_players
                    db.update_server_list(db_server.name, db_server.total_players, db_server.timestamp, uptime=db_server.uptime, min30_chest_count=db_server.min30_chest_count, chest_count=db_server.chest_count, last_chest_count=db_server.last_chest_count)

                await asyncio.sleep(30)
    
    async def chest_count_check(self):
        async with Corkus() as corkus:
            while True:
                db_server_list = db.get_server_list_all()

                db_server_list_5_plus = [db_server.name for db_server in db_server_list if int(db_server.uptime) >= 300]
                
                onlineplayers = await corkus.network.online_players()
                serverlist = onlineplayers.servers
                
                chosen_server_list = [server for server in serverlist if server.name in db_server_list_5_plus]

                players_chests_found = {}

                for chosen_server in chosen_server_list:
                    partial_players = chosen_server.players
                    for partial_player in partial_players:
                        player = await partial_player.fetch()
                        player_chests_found = player.statistics.chests_found
                        players_chests_found[player.username] = player_chests_found

                    db_server = [db_server for db_server in db_server_list if db_server.name == chosen_server.name][0]
                    if db_server.chest_count == None:
                        db_server.chest_count = players_chests_found

                    keys_to_delete = [key for key in db_server.chest_count if not (key in players_chests_found)]
            
                    for key in keys_to_delete:
                        del db_server.chest_count[key]
            
                    keys_to_delete = [key for key in players_chests_found if not (key in db_server.chest_count)]
            
                    for key in keys_to_delete:
                        del players_chests_found[key]
                    
                    chest_count = json.loads(db_server.chest_count)

                    c_db_server_chest_count = Counter(chest_count)
                    c_players_chests_found = Counter(players_chests_found)
                    server_total_chests_found = c_players_chests_found - c_db_server_chest_count

                    db_server.min30_chest_count = server_total_chests_found
                    db_server.last_chest_count = chest_count
                    db_server.chest_count = players_chests_found

                    db.update_server_list(db_server.name, db_server.total_players, db_server.timestamp, uptime=db_server.uptime, min30_chest_count=db_server.min30_chest_count, chest_count=json.dumps(db_server.chest_count), last_chest_count=json.dumps(db_server.last_chest_count))

                await asyncio.sleep(1800)


