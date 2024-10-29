# Python imports
import random

from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.move import Move

# Internal imports
from blokus.player.base_player import BasePlayer


class GreedyBot(BasePlayer):
    """This bot plays with a greedy style,
    it always plays the biggest possible piece.
    If multiple pieces are possible it will randomly
    select between them.
    """

    def select_best_move(self, moves: list[Move]) -> Move:
        """Selects a random move

        Args:
            moves (list[Move]): moves to select from

        Returns:
            Move: randomly selected move
        """
        random.shuffle(moves)
        biggest_move = max(moves, key=lambda x: len(x.idxs))
        biggest_moves = [move for move in moves if len(move.idxs) == len(biggest_move.idxs)]
        # find biggest dimensinon
        return random.choice(biggest_moves)
