
# Python Imports
from enum import Enum
# Extenral Imports
# Intenral Imports

class PieceTypeEnum(Enum):
    def __init__(self, id, cls):
        self.id = id
        self.cls = cls
    SINGLE = "single", 
    DOUBLE = "double"
    STAIGHT_TRIPLE = "straight_triple"
    L_TRIPLE = ""
    BLUE: 4