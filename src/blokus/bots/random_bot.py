# Python imports
import random

from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.move import Move

# Internal imports
from blokus.player.base_player import BasePlayer


class RandomBot(BasePlayer):
    """This bot plays randomly simply selecting any of the valid moves"""

    def select_best_move(self, moves: list[Move]) -> Move:
        """Selects a random move

        Args:
            moves (list[Move]): moves to select from

        Returns:
            Move: randomly selected move
        """
        return random.choice(moves)
