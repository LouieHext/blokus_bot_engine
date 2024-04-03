# Python Imports
from dataclasses import dataclass

# External Imports
# Internal Imports
from blokus.board_states import BoardStatesEnum
from blokus.pieces.base import BasePiece


@dataclass
class Move:
    """
    Represents a move on the board,
    this includes:
    - the colour of player
    - the piece name
    - the indexes on the board where the piece is placed
    """

    colour: BoardStatesEnum
    piece: BasePiece
    idxs: list[tuple[int]]
