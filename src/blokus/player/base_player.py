from abc import ABC, abstractmethod

from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.move import Move


class BasePlayer(ABC):
    """Abstract base class for the Player.

    Each player must specifiy the method `select_best_move`

    """

    def __init__(self, board: Board, colour: BoardStatesEnum):
        """initialiser for player class

        Args:
            board (Board): board the game is being played on
            colour (BoardStatesEnum): colour of the player
        """
        self.board = board
        self.colour = colour

    @abstractmethod
    def select_best_move(self, moves: list[Move], board:Board) -> Move:
        """Given a selection of valid moves, returns the move
        that the player thinks is best according to its internal logic.

        Args:
            moves (list[Move]): List of valid moves

        Returns:
            Move: Move to play
        """
