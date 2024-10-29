# Python Imports
from dataclasses import dataclass

# External Imports
import numpy as np

# Internal Imports
from blokus.board_states import BoardStatesEnum
from blokus.pieces.piece_names import PieceNameEnum


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
    piece_type: PieceNameEnum
    idxs: list[tuple[int]]

    @classmethod
    def from_piece_representation(
        cls,
        colour: BoardStatesEnum,
        piece_type: PieceNameEnum,
        relative_representation: list[tuple[int]],
        origin: tuple[int],
    ) -> "Move":
        """Creates a move from a piece representation

        Args:
            colour (BoardStatesEnum): colour of the player
            piece_type (PieceNameEnum): type of the piece
            piece (list[str]): piece representation

        Returns:
            Move: the move
        """
        # Get the indexes of the piece
        idxs = [(idx_pair[0] + origin[0], idx_pair[1] + origin[1]) for idx_pair in relative_representation]
        return cls(colour, piece_type, idxs)


    def __hash__(self) -> int:
        return hash((self.colour, self.piece_type, tuple(self.idxs)))