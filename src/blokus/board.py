# Python Imports
# Extenral Imports
import matplotlib.pyplot as plt
import numpy as np

# Intenral Imports
from blokus.board_states import BoardStatesEnum
from blokus.exceptions import InvalidMove
from blokus.move import Move
from blokus.pieces.piece_set import build_full_piece_set


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
        self.piece_sets = self._get_initial_piece_dict()

    @property
    def array(self) -> np.ndarray:
        """Returns the state of the board as a nxn interger array,
        the ints map to the colours via the BoardStatesEnum.

        Returns:
            np.ndarray: current state of the board
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
        self.piece_sets[move.colour].remove_piece_by_name(move.piece_type)

    def display_board(self):
        """Displays the board via matplotlib"""
        plt.imshow(self.array)
        plt.show()

    def get_valid_moves_for_colour(self, colour: BoardStatesEnum) -> list[Move]:
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

    def check_move_validity(
        self, move: Move, return_at_first_fail: bool = True, validation_methods: list[callable] = None
    ) -> list[str]:
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
            validation_methods (list[callable]): Methods to validate agaist, defaults to None

        Returns:
            list[str]: the errors of the move
        """
        error_list = []
        # validation methods, hard code
        if not validation_methods:
            validation_methods = [
                self._validate_in_bounds,
                self._validate_unused_piece,
                self._validate_corner_relation,
                self._validate_overlap,
                self._validate_edge_relation,
            ]
        # check each method, tracking errors as we go
        for validation_method in validation_methods:
            try:
                validation_method(move)
            except InvalidMove as e:
                error_list.append(e)
            if error_list and return_at_first_fail:
                return error_list
            # if out of bounds other checks are nonsensical and might break
            if validation_method == self._validate_in_bounds and error_list:
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
        error_list = self.check_move_validity(move)
        return not error_list

    def check_if_corner_idx(self, idx: tuple[int]) -> bool:
        """Checks if the supplied idx is the corner of a board.

        Args:
            idx (tuple[int]): idx to check

        Returns:
            bool: if the supplied idx is a corner
        """
        # checks if an idx is a corner idx.
        corner_idxs = [(0, 0), (0, self.dimension), (self.dimension, 0), (self.dimension, self.dimension)]
        return idx in corner_idxs

    def get_diagonal_idxs_from_idx(self, idx: tuple[int]) -> list[tuple[int]]:
        """Gets the diagonal idxs from a given index.
        These are +/- 1 for row and column.

        Additionally checks that we are in the bounds

        Args:
            idx (tuple[int]): index to check

        Returns:
            list[tuple[int]]: diagonal indices
        """
        # diagonal neighbours are +- 1 in both idxs
        row, col = idx
        diagonal_idxs = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                diagonal_idxs.append((row + x, col + y))
        # remove any that are out of bounds
        diagonal_idxs = [idx_pair for idx_pair in diagonal_idxs if self.check_coord_in_board(idx_pair)]
        return diagonal_idxs

    def get_adjacent_idxs_from_idx(self, idx: tuple[int]) -> list[tuple[int]]:
        """Gets the adjacent idxs from a given index.
        These are +/- 1 for row and column but never both

        Additionally checks that we are in the bounds

        Args:
            idx (tuple[int]): index to check

        Returns:
            list[tuple[int]]: diagonal indices
        """
        # diagonal neighbours are +- 1 in both idxs
        row, col = idx
        adjacent_idxs = []
        for x in [-1, 1]:
            adjacent_idxs.append((row + x, col))
        for y in [-1, 1]:
            adjacent_idxs.append((row, col + y))

        # remove any that are out of bounds
        adjacent_idxs = [idx_pair for idx_pair in adjacent_idxs if self.check_coord_in_board(idx_pair)]
        return adjacent_idxs

    def check_coord_in_board(self, coord_pair: tuple[int]) -> bool:
        """Checks that a given coord pair exists within the board.


        Args:
            coord_pair (tuple[int]): coord_pair to check

        Returns:
            bool : if the coord pair is in the board
        """
        return all([0 <= coord <= self.dimension for coord in coord_pair])

    def _validate_piece_idx_matches_type(self, move: Move):
        """Validates that the idx of the move match the topology of the piece
        in the move

        Args:
            move (Move): move to check

        Raises:
            InvalidMove: if the mnove idxs to match the move piece type
        """
        # check if the idx matches the shape
        piece = self.piece_sets[move.colour].get_piece_by_name(move.piece_type)
        # convert move idxs into a relative map
        binary_representation = self._get_binary_representation_from_move(move)
        # check if this map exists in the piece representations
        if binary_representation not in piece.all_idx_representations:
            raise InvalidMove(f"The supplied idx do not match the piece type shape {move}")

    def _validate_unused_piece(self, move: Move):
        """Validates if the piece associated with the move
        has not yet been used by the colour

        Args:
            move (Move): Move to validate

        Raises:
            InvalidMove: if the piece has already been used
        """
        if move.piece_type in self.piece_sets[move.colour].present_types:
            return
        raise InvalidMove(f"The piece {move.piece_type} was already used by {move.colour}")

    def _validate_overlap(self, move: Move):
        """Checks if the move is trying to place on an already populated grid cell

        Args:
            move (Move): Move to validate

        Raises:
            InvalidMove: if the move overalsp an existing piece
        """
        # check the move against the board array
        for idx_pair in move.idxs:
            row, col = idx_pair
            if self.array[row][col]:
                raise InvalidMove(f"cell {row,col} is already populated")

    def _validate_corner_relation(self, move: Move):
        """Validates that the move obeys the corner touching relation.
        Each new piece must touch the corner of another piece

        Args:
            move (Move): move to check
        """
        # checks that diagonal neighbours of the any of the moves
        # idxs are from the same colourillegal_move
        for idx in move.idxs:
            # if its the first move in a corner this is obeyed
            if self.check_if_corner_idx(idx):
                return
            diagonal_neighbours = self.get_diagonal_idxs_from_idx(idx)
            for diagonal_neighbour in diagonal_neighbours:
                row, col = diagonal_neighbour
                # check if corner relation obeyed
                if self.array[row][col] == move.colour.value:
                    return
        raise InvalidMove(f"The move does not obey the corner relation, {move}")

    def _validate_edge_relation(self, move: Move):
        """Checks that the move obeys the side relation rule.
        This rule prevents moves that share a side border
        with an existing piece of the same colour

        Args:
            move (Move): move to check

        Raises:
            InvalidMove: if the move does not obey the side relation rules
        """
        # checks that the move does not share any borders with existing moves of
        # the colour
        for idx in move.idxs:
            # get neighbours
            adjacent_neighbours = self.get_adjacent_idxs_from_idx(idx)
            for adjacent_neighbour in adjacent_neighbours:
                # check each
                row, col = adjacent_neighbour
                if self.array[row][col] == move.colour.value:
                    raise InvalidMove(f"The move does not objey the side relation, {move}")

    def _validate_in_bounds(self, move: Move):
        """Checks that the move is fully contained within the board

        Args:
            move (Move): move to check

        Raises:
            InvalidMove: if the move does not fit within the board
        """
        if any(not self.check_coord_in_board(idx) for idx in move.idxs):
            raise InvalidMove(f"Move does not fit in the board, {move}")

    def _get_initial_piece_dict(self) -> dict:
        """Gets the initial dictionary of all the pieces
        the keys are the colours,
        the values are the list of all piece enums
        Returns:
            dict: all piece enums for each colour
        """
        return {
            BoardStatesEnum.RED: build_full_piece_set(),
            BoardStatesEnum.GREEN: build_full_piece_set(),
            BoardStatesEnum.YELLOW: build_full_piece_set(),
            BoardStatesEnum.BLUE: build_full_piece_set(),
        }

    def _get_empty_board(self) -> np.ndarray:
        """Returns an empty array to represent the board.
        The board is represented as a nxn array of ints

        Returns:
            np.ndarray: empty board of zeros
        """
        return np.zeros((self.dimension, self.dimension), dtype=int)

    def _get_binary_representation_from_move(self, move: Move) -> np.ndarray:
        pass
