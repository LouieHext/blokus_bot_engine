# Internal Imports
from blokus.player.local_player import LocalPlayer
from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.bots.bot_enums import BotEnum


class PlayerFactory:
    @staticmethod
    def build_local_player_from_enum(board: Board, colour: BoardStatesEnum, bot_enum:BotEnum) ->LocalPlayer:
        """Builds a local player from the supplied enum

        Args:
            board (Board): board to link to player
            colour (BoardStatesEnum): colour of player
            bot_enum (BotEnum): bot enum to use

        Returns:
            LocalPlayer: local player
        """
        return bot_enum.cls(board,colour)