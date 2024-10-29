# Python Imports
from enum import Enum

# Extenral Imports
# Intenral Imports


class BoardStatesEnum(Enum):
    def __init__(self, int_id: int, str_id: str):
        self.int_id = int_id
        self.str_id = str_id

    EMPTY = 0, "empty"
    RED = 1, "red"
    GREEN = 2, "green"
    YELLOW = 3, "yellow"
    BLUE = 4, "blue"

    @classmethod
    def get_player_colours(cls) -> list["BoardStatesEnum"]:
        """Gets the colours of players

        Returns:
            list["BoardStatesEnum"]: list of board state enums
        """
        return [cls.RED, cls.BLUE, cls.GREEN, cls.YELLOW]
