# Python Imports
# Extenral Imports
import matplotlib.pyplot as plt
import matplotlib as mpl
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

    def __init__(self, dimension: int = 20):
        self.__dimension = dimension
        self.__array = self._get_empty_board()
        self.piece_sets = self._get_initial_piece_dict()
        self.moves_checked = {BoardStatesEnum.RED: [], BoardStatesEnum.GREEN: [], BoardStatesEnum.YELLOW: [], BoardStatesEnum.BLUE: []}

    @property
    def array(self) -> np.ndarray:
        """Returns the state of the board as a nxn interger array,
        the ints map to the colours via the BoardStatesEnum.

        Returns:
            np.ndarray: current state of the board
        """
        return self.__array
    
    @property
    def flat_array(self) -> np.ndarray:
        """Returns the state of the board as a flat array

        Returns:
            np.ndarray: flat array of the board
        """
        return self.array.flatten()

    @property
    def dimension(self) -> int:
        """returns the dimension of the board,
        the board is nxn where is is the dimension

        Returns:
            int: dimensino of the board
        """
        return self.__dimension
    @property
    def arr_dimension(self) -> int:
        """Returns the dimension of the array

        Returns:
            int: dimension of the array
        """
        return self.__dimension -1
    @property
    def corner_idxs(self) -> list[tuple[int]]:
        """Returns the corner idxs of the board.

        Returns:
            list[tuple[int]]: corner idxs
        """
        corner_idxs = [(0, 0), (0, self.arr_dimension), (self.arr_dimension, 0), (self.arr_dimension, self.arr_dimension)]
        return corner_idxs

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
        cmaplist = ["grey","red","green","yellow","blue"]
        cmap = mpl.colors.LinearSegmentedColormap.from_list('blokus', cmaplist, 5)
        bounds = np.linspace(0,4,5)
        norm = mpl.colors.BoundaryNorm(bounds, 4)
        plt.imshow(self.array, cmap = cmap, norm = norm)
        plt.show(block = False)
        plt.pause(1e-5)
        plt.clf()

    def display_move(self, move: Move):
        """Displays the move on the board via matplotlib

        Args:
            move (Move): move to display
        """
        temp_array = self._get_empty_board()
        for idx_pair in move.idxs:
            row, col = idx_pair
            temp_array[row][col] = move.colour.value
        plt.figure()
        plt.imshow(self.array,cmap="binary")
        plt.figure()
        plt.imshow(temp_array,cmap="copper")
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
        # find all corners for the colour
        # find the origin associated with the corner
        # for each piece, check all variants
        valid_moves = self._find_valid_moves_brute_force(colour)
        return valid_moves
    
    def _find_valid_moves_brute_force(self, colour: BoardStatesEnum) -> list[Move]:
        """Finds all valid moves for the colour via brute force.
        This finds all possible origins for the colour, then for each origin
        checks all possible piece placements.
        Valid moves are then returned.

        Args:
            colour (BoardStatesEnum): colour to find moves for

        Returns:
            list[Move]: list of valid moves
        """
        valid_moves = []
        possible_origins = self._get_possible_origins_for_colour(colour)
        count = 0
        for origin in possible_origins:
            for piece in self.piece_sets[colour].pieces:
                for piece_rep in piece.all_idx_representations:
                    count += 1
                    # build move from representation
                    move = Move.from_piece_representation(colour, piece.name, piece_rep, origin)
                    # check if the piece can be placed
                    if self.validate_move(move):
                        valid_moves.append(move)
        self.moves_checked[colour].append(count)
        return valid_moves

    def _get_possible_origins_for_colour(self, colour: BoardStatesEnum) -> list[tuple[int]]:
        """Returns all possible origins for the colour.
        Each origin is associated with a corner of a piece of the colour.

        Args:
            colour (BoardStatesEnum): colour to get origins for

        Returns:
            list[tuple[int]]: list of all possible origins
        """
        # if the colour has no pieces on the board, return any free corner
        if not any(value == colour.value for value in self.flat_array):
            empty_corners = [corner for corner in self.corner_idxs if not self.array[corner[0]][corner[1]]]
            return empty_corners
        # get all the corners for the colour
        corner_idxs = self._get_corner_idxs_for_colour(colour)
        # get all the origins for the corners
        origins = []
        for corner in corner_idxs:
            origins += self._get_valid_origins_from_corner(corner,colour)
        return origins
    
    def _get_valid_origins_from_corner(self, corner: tuple[int],colour: BoardStatesEnum) -> list[tuple[int]]:
        """Returns all valid origins from a corner.
        This is all the diagonals from the corner

        Args:
            corner (tuple[int]): corner to get origins from

        Returns:
            list[tuple[int]]: list of all valid origins
        """
        # get all the diagonals from the corner
        possible_origins =  self.get_diagonal_idxs_from_idx(corner)
        valid_origins = []
        for origin in possible_origins:
            # remove any that are already populated
            if self.array[origin[0]][origin[1]]:
                continue
            # get the adjacent neighbours
            adjacent_neighbours = self.get_adjacent_idxs_from_idx(origin)
            # check if any of the neighbours are the same colour
            if any(self.array[neighbour[0]][neighbour[1]] == colour.value for neighbour in adjacent_neighbours):
                continue

            valid_origins.append(origin)
        return valid_origins

    def _get_corner_idxs_for_colour(self, colour: BoardStatesEnum) -> list[tuple[int]]:
        """Returns all the corner idxs for the colour

        Args:
            colour (BoardStatesEnum): colour to get corners for

        Returns:
            list[tuple[int]]: list of corner idxs
        """
        corner_idxs = []
        check_sum = 0
        for row in range(self.dimension):
            for col in range(self.dimension):
                check_sum += 1
                # if the cell is not the colour, skip
                if not self.array[row][col] == colour.value:
                    continue
                # find the horizontal and vertical neighbours
                vertical_neighbours = [(row, col - 1), (row, col + 1)]
                vertical_neighbours = [idx for idx in vertical_neighbours if self.check_coord_in_board(idx)]
                horizontal_neighbours = [(row - 1, col), (row + 1, col)]
                horizontal_neighbours = [idx for idx in horizontal_neighbours if self.check_coord_in_board(idx)]
                horizonal_score = sum([self.array[_row][_col] == colour.value for _row, _col in horizontal_neighbours])
                vertical_score = sum([self.array[_row][_col] == colour.value for _row, _col in vertical_neighbours])
                # account for game borders
                if row in [0, self.arr_dimension]:
                    horizonal_score += 1
                if col in [0, self.arr_dimension]:
                    vertical_score += 1
                # corner has only 1 neighbour in vertical or horizontal
                if horizonal_score >1 or vertical_score > 1:
                    continue
                corner_idxs.append((row, col))
        return corner_idxs

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
        return idx in self.corner_idxs

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
        return all([0 <= coord <= self.arr_dimension for coord in coord_pair])

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
