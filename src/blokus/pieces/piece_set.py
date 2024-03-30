# Python Imports
from dataclasses import dataclass, field

# Extenral Imports
# Intenral Imports
from blokus.pieces.base import BasePiece
from blokus.pieces.piece_names import PieceNameEnum
from blokus.pieces.pieces import *


@dataclass
class PieceSet:
    pieces: list[BasePiece] = field(default_factory=list)

    def remove_piece_by_name(self, name: PieceNameEnum):
        """Removes a piece from the set by name

        Args:
            name (PieceNameEnum): name of the piece to remove
        """
        for piece in self.pieces:
            if piece.name == name:
                self.pieces.remove(piece)


def build_full_piece_set() -> PieceSet:
    """Builds a full set of pieces

    Returns:
        PieceSet: a full set of pieces
    """
    return PieceSet(pieces=[I1, I2, I3, I4, I5, L4, L5, T4, T5, Z4, Z5, V3, V5, F, X, U, N, W, O, P, Y])
