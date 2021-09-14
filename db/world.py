import time
from corkus import Corkus

class World:
    def __init__(self, name, total_players, timestamp, uptime="", min30_chest_count=None, chest_count=None, last_chest_count=None):
        self.name = name
        self.total_players = total_players
        self.timestamp = timestamp
        self.chest_count = chest_count
        self.last_chest_count = last_chest_count
        self.min30_chest_count = min30_chest_count
        self.uptime = uptime
    
    def calculate_30mins_chest_count(self):
        self.min30_chest_count = self.chest_count - self.last_chest_count

    def calculate_uptime(self):
        self.uptime = str(int(int(time.time()) - self.timestamp)/60) + " minutes"

    async def update_total_players(self):
        async with Corkus() as corkus:
            onlineplayers = await corkus.network.online_players()
            serverlist = onlineplayers.servers
            for server in serverlist:
                if server.name == self.name:
                    self.total_players == server.total_players