# Python Imports
# Extenral Imports
import numpy as np

from blokus.pieces.base import BasePiece

# Intenral Imports
from blokus.pieces.piece_names import PieceNameEnum

I1_array = [1]
I2_array = [
    [0, 0, 0],
    [0, 1, 1],
    [0, 0, 0],
]
I3_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
I4_array = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
I5_array = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]

I1 = BasePiece(base_binary_repr=np.array(I1_array), name=PieceNameEnum.I1)
I2 = BasePiece(base_binary_repr=np.array(I2_array), name=PieceNameEnum.I2)
I3 = BasePiece(base_binary_repr=np.array(I3_array), name=PieceNameEnum.I3)
I4 = BasePiece(base_binary_repr=np.array(I4_array), name=PieceNameEnum.I4)
I5 = BasePiece(base_binary_repr=np.array(I5_array), name=PieceNameEnum.I5)
