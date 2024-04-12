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
L4_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
L5_array = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
T4_array = [
    [0, 0, 1],
    [0, 1, 1],
    [0, 0, 1],
]
T5_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0],
]

Z4_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
Z5_array = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
V3_array = [
    [0, 0, 1],
    [0, 1, 1],
    [0, 0, 0],
]
V5_array = [
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
F_array = [
    [0, 0, 0, 1, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

P_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

X_array = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]
U_array = [
    [0, 1, 1],
    [0, 1, 0],
    [0, 1, 1],
]
N_array = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
W_array = [
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
O_array = [
    [0, 1, 1],
    [0, 1, 1],
    [0, 0, 0],
]
P_array = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]
Y_array = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


# I pieces
I1 = BasePiece(base_binary_repr=np.array(I1_array), name=PieceNameEnum.I1)
I2 = BasePiece(base_binary_repr=np.array(I2_array), name=PieceNameEnum.I2)
I3 = BasePiece(base_binary_repr=np.array(I3_array), name=PieceNameEnum.I3)
I4 = BasePiece(base_binary_repr=np.array(I4_array), name=PieceNameEnum.I4)
I5 = BasePiece(base_binary_repr=np.array(I5_array), name=PieceNameEnum.I5)
# L pieces
L4 = BasePiece(base_binary_repr=np.array(L4_array), name=PieceNameEnum.L4)
L5 = BasePiece(base_binary_repr=np.array(L5_array), name=PieceNameEnum.L5)
# T pieces
T4 = BasePiece(base_binary_repr=np.array(T4_array), name=PieceNameEnum.T4)
T5 = BasePiece(base_binary_repr=np.array(T5_array), name=PieceNameEnum.T5)
# Z pieces
Z4 = BasePiece(base_binary_repr=np.array(Z4_array), name=PieceNameEnum.Z4)
Z5 = BasePiece(base_binary_repr=np.array(Z5_array), name=PieceNameEnum.Z5)
# V pieces
V3 = BasePiece(base_binary_repr=np.array(V3_array), name=PieceNameEnum.V3)
V5 = BasePiece(base_binary_repr=np.array(V5_array), name=PieceNameEnum.V5)
# Other pieces
F = BasePiece(base_binary_repr=np.array(F_array), name=PieceNameEnum.F)
X = BasePiece(base_binary_repr=np.array(X_array), name=PieceNameEnum.X)
U = BasePiece(base_binary_repr=np.array(U_array), name=PieceNameEnum.U)
N = BasePiece(base_binary_repr=np.array(N_array), name=PieceNameEnum.N)
W = BasePiece(base_binary_repr=np.array(W_array), name=PieceNameEnum.W)
O = BasePiece(base_binary_repr=np.array(O_array), name=PieceNameEnum.O)
P = BasePiece(base_binary_repr=np.array(P_array), name=PieceNameEnum.P)
Y = BasePiece(base_binary_repr=np.array(Y_array), name=PieceNameEnum.Y)

