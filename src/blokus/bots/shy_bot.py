#Python imports
import random
#Internal imports
from blokus.player.base_player import BasePlayer
from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.move import Move


class ShyBot(BasePlayer):
    """This bot plays with a shy style,
    it always plays the smallest possible piece. 
    If multiple pieces are possible it will randomly
    select between them.
    """

    def __init__(self, board: Board, colour: BoardStatesEnum):
        """initialiser for shy bot, simply calls base

        Args:
            board (Board): board the game is being played on
            colour (BoardStatesEnum): colour of the player
        """
        super().__init__(board, colour)

    def select_best_move(self, moves: list[Move]) -> Move:
        """Selects a random move

        Args:
            moves (list[Move]): moves to select from

        Returns:
            Move: randomly selected move
        """
        smallest_move =  min(moves, key=lambda x: len(x.idxs))
        smallest_moves = [move for move in moves if len(move.idxs) == len(smallest_move.idxs)]
        return random.choice(smallest_moves)