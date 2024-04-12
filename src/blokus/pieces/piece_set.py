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
                return

    def __contains__(self, piece: BasePiece) -> bool:
        return piece in self.pieces

    @property
    def present_types(self) -> list[PieceNameEnum]:
        """Returns the name enums of all pieces in this piece set

        Returns:
            list[PieceNameEnum]: piece name enums
        """
        return [piece.name for piece in self.pieces]

    def get_piece_by_name(self, name: PieceNameEnum) -> BasePiece:
        """Returns the piece in the set that matches the supplied name,
        raising an error if no piece matches the name

        Args:
            name (PieceNameEnum): name to find piece for

        Raises:
            ValueError: if no pirce has the supplied name

        Returns:
            BasePiece: piece that matches the name
        """
        if name not in self.present_types:
            raise ValueError(f"{name} is not in the present pieces of this set")
        piece = [p for p in self.pieces if p.name == name][0]
        return piece


def build_full_piece_set() -> PieceSet:
    """Builds a full set of pieces

    Returns:
        PieceSet: a full set of pieces
    """
    full_list = [I1, I2, I3, I4, I5, L4, L5, T4, T5, Z4, Z5, V3, V5, F, X, U, N, W, O, P, Y]
    return PieceSet(pieces=full_list)
