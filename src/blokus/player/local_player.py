# Internal Imports
from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.player.base_player import BasePlayer


class LocalPlayer(BasePlayer):
    def __init__(self, board: Board, colour: BoardStatesEnum):
        """initialiser for player class

        Args:
            board (Board): board the game is being played on
            colour (BoardStatesEnum): colour of the player
        """
        super().__init__(board, colour)
