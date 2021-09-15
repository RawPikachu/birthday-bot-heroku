import time

class World:
    def __init__(self, name, total_players, timestamp, uptime="", min30_chest_count=None, chest_count=None, last_chest_count=None):
        self.name = name
        self.total_players = total_players
        self.timestamp = timestamp
        self.chest_count = chest_count
        self.last_chest_count = last_chest_count
        self.min30_chest_count = min30_chest_count
        self.uptime = uptime
    
    def calculate_30mins_chest_count(self, chest_count):
        if self.chest_count == None:
            self.chest_count = chest_count
        self.min30_chest_count = chest_count - self.chest_count
        self.last_chest_count = self.chest_count
        self.chest_count = chest_count

    def calculate_uptime(self):
        self.uptime = int((int(time.time()) - self.timestamp)/60)