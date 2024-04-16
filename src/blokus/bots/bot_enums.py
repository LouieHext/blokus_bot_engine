# Python Imports
from enum import Enum

# Extenral Imports
# Intenral Imports
from blokus.player.base_player import BasePlayer
from blokus.bots.random_bot import RandomBot
from blokus.bots.greedy_bot import GreedyBot
from blokus.bots.shy_bot import ShyBot

class BotEnum(Enum):
    def __init__(self, cls:BasePlayer):
        self.cls = cls

    RANDOM = RandomBot
    GREEDY = GreedyBot
    SHY = ShyBot

  