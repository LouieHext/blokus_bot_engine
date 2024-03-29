
# Python Imports
# Extenral Imports
import numpy as np
# Intenral Imports
from blokus_sim.board_states import BoardStatesEnum
from blokus_sim.move import Move
from blokus_sim.piece_types import PieceTypeEnum
from blokus_sim.exceptions import InvalidMove

class Board:
    """
    This class represents the blokus board.
    The board is represnted as a nxn int array via numpy.
    The ints in the array are mapped to the colours via the BoardStatesEnum

    The class is able to get the valid moves for a given colour

    additionally the board supports plotting
    """
    def __init__(self, dimension: int = 16):
        self.__dimension = dimension
        self.__array = self._get_empty_board()
        self.remaining_pieces_dict = self._get_initial_piece_dict()

    @property
    def array(self) -> np.ndarry:
        """Returns the state of the board as a nxn interger array,
        the ints map to the colours via the BoardStatesEnum.

        Returns:
            np.ndarry: current state of the board
        """
        return self.__array
    
    @property
    def dimension(self) -> int:
        """returns the dimension of the board,
        the board is nxn where is is the dimension

        Returns:
            int: dimensino of the board
        """
        return self.__dimension
    
    def play_move(self, move: Move):
        """Validates the move and if it is valid plays it on the board

        Args:
            move (Move): move to play on board

        Raises:
            InvalidMove: If the move played was invalid
        """
        move_errors = self.check_move_validity(move)
        if move_errors:
            raise InvalidMove(f"supplied Move is invalid due to {move_errors}")
        for idx_pair in move.idxs:
            row, col = idx_pair
            self.__array[row][col] = move.colour.value
        self.remaining_pieces_dict[move.colour].remove(move.piece_type)

    def get_valid_moves_for_colour(self, colour:BoardStatesEnum) -> list[Move]:
        """
        Returns a list of all valid moves for the supplied colour.
        This takes into the account the board state and the remaining
        moves pieces of the colour

        Args:
            colour (BoardStatesEnum): colour to get valid moves from

        Returns:
            list[Move]: list of valid moves
        """
        raise NotImplementedError
    
    def check_move_validity(self, move: Move, return_at_first_fail:bool = False) -> list[str]:
        """Checks the move validity, if there are any issues returns the associated
        erorr strings.

        this checks that
         - the piece has not been use before
         - the move does not overlap with existing pieces
         - the move touches a corner of an existing piece of the colour
         - the move does not touch any flat edges of existing pieces of the colour

        Args:
            move (Move): move to validate
            return_at_first_fail (bool): whether to exit early if an issue is detcted,
                                         Defaults to False

        Returns:
            list[str]: the errors of the move
        """
        error_list = []
        # validation methods, hard code
        validation_methods = [self._validate_unused_piece]
        # check each method, tracking errors as we go
        for validation_method in validation_methods:
            try:
                validation_method(move)
            except InvalidMove as e:
                error_list.append(e)
            if error_list and return_at_first_fail:
                return error_list
        # return error list
        return error_list
    
    def validate_move(self, move: Move) -> bool:
        """Validates that a move meets the rule requirements
        for the current board state.

        This does not raise any erorrs or return reasons for
        False moves. Use `check_move_validity` for that.

        Args:
            move (Move) move to check

        Returns:
            bool: True if the move is valid, False otherwise
        """
        error_list =  self.check_move_validity(move)
        return not error_list
                
    def _validate_unused_piece(self, move: Move):
        """Validates if the piece associated with the move
        has not yet been used by the colour

        Args:
            move (Move): Move to validate

        Raises:
            InvalidMove: if the piece has already been used
        """
        if move.piece_type in self.remaining_pieces_dict[move.colour]:
            return
        raise InvalidMove(f"The piece {move.piece_type} was already used by {move.colour}")
    
    def _get_initial_piece_dict(self) -> dict:
        """Gets the initial dictionary of all the pieces
        the keys are the colours,
        the values are the list of all piece enums
        Returns:
            dict: all piece enums for each colour
        """
        return  {
            BoardStatesEnum.RED: list(PieceTypeEnum),
            BoardStatesEnum.GREEN: list(PieceTypeEnum),
            BoardStatesEnum.YELLOW: list(PieceTypeEnum),
            BoardStatesEnum.BLUE: list(PieceTypeEnum),
        }
    
    def _get_empty_board(self) -> np.ndarry:
        """Returns an empty array to represent the board.
        The board is represented as a nxn array of ints

        Returns:
            np.ndarry: empty board of zeros
        """
        return np.zeros((self.dimension,self.dimension), dtype = int)