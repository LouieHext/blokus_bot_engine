# Python Imports
from enum import Enum

from blokus.bots.greedy_bot import GreedyBot
from blokus.bots.random_bot import RandomBot
from blokus.bots.shy_bot import ShyBot

from blokus.player.base_player import BasePlayer

from blokus.bots.corner_bot import CornerBot

from blokus.bots.potential_bot import PotentialBot

class BotEnum(Enum):
    def __init__(self, cls: BasePlayer):
        self.cls = cls

    RANDOM = RandomBot
    GREEDY = GreedyBot
    SHY = ShyBot
    CORNER = CornerBot
    POTENTIAL = PotentialBot
