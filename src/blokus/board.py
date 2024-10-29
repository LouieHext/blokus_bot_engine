# Python Imports
# Extenral Imports
from calendar import c
from copy import copy, deepcopy
from functools import cache, cached_property
from typing import Self
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Intenral Imports
from blokus.board_states import BoardStatesEnum
from blokus.exceptions import InvalidMove
from blokus.move import Move
from blokus.pieces.piece_set import build_full_piece_set

from blokus.pieces.piece_set import PieceSet


class Board:
    """
    This class represents the blokus board.
    The board is represnted as a nxn int array via numpy.
    The ints in the array are mapped to the colours via the BoardStatesEnum

    The class is able to get the valid moves for a given colour

    additionally the board supports plotting
    """

    def __init__(self, dimension: int = 20, board_array: np.ndarray = None, piece_set: dict[BoardStatesEnum, PieceSet] = None):
        self.__dimension = dimension

        self.__array = board_array if board_array is not None else self._get_empty_board()
        self.__piece_sets = piece_set if piece_set is not None else self._get_initial_piece_dict()
        
        self.__valid_moves_dict: dict[BoardStatesEnum, list[Move]] = {colour: [] for colour in BoardStatesEnum.get_player_colours()}
        self.__latest_move = None
        self.__move_list: list[Move] = []

    def create_future_board_from_move(self, move: Move) -> Self:
        """Creates a future board from a move

        Args:
            board (Board): board to create from
            move (Move): move to play

        Returns:
            Board: future board
        """
        new_board = np.copy(self.array)

        for idx_pair in move.idxs:
            row, col = idx_pair
            new_board[row][col] = move.colour.int_id

        # create new piece set, only copying the pieces being removed
        new_piece_set = {colour: piece_set for colour, piece_set in self.piece_sets.items() if colour != move.colour}
        new_piece_set[move.colour] = PieceSet(pieces = [piece for piece in self.piece_sets[move.colour].pieces if piece.name != move.piece_type])
        
        future_board = Board(self.dimension, new_board, new_piece_set)
        
        return future_board

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
            self.__array[row][col] = move.colour.int_id

        self.__piece_sets[move.colour].remove_piece_by_name(move.piece_type)

        self.__latest_move = move
        self.__move_list.append(move)
        self._update_valid_moves()

    def get_score_for_colour(self, colour: BoardStatesEnum) -> int:
        """For the supplied colour gets the score.
        The score is how many cells of the board are active

        Args:
            colour (BoardStatesEnum): colour to find score for

        Returns:
            int: score
        """
        score = sum([value == colour.int_id for value in self.flat_array])
        return score

    def get_score_str(self) -> str:
        """Returns the score str, this has each colour
        and its associated score

        Returns:
            str: score string
        """
        score_str = ""
        for colour in BoardStatesEnum.get_player_colours():
            score_str += f"{colour.str_id}: {self.get_score_for_colour(colour)} "

        return score_str

    def display_board(self, stop_code: bool = False):
        """Displays the board and the scores

        Args:
            stop_code (bool, optional): if the plot should stop the code. Defaults to False.
        """
        cmaplist = ["grey", "red", "green", "yellow", "blue"]
        cmap = mpl.colors.LinearSegmentedColormap.from_list("blokus", cmaplist, 5)
        bounds = np.linspace(0, 4, 5)
        norm = mpl.colors.BoundaryNorm(bounds, 4)

        plt.imshow(self.array, cmap=cmap, norm=norm,extent=[0, self.dimension, 0, self.dimension],alpha=0.8)
        plt.gca().set_xticks(np.arange(0, self.dimension, 1))
        plt.gca().set_yticks(np.arange(0, self.dimension, 1))
        plt.grid(visible=True, color="black", linestyle="-", linewidth=0.7, alpha=0.4)
        plt.gca().tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # make even grid
        plt.gca().set_aspect("equal", adjustable="box")
        plt.title(self.get_score_str())
        plt.show(block=stop_code)
        plt.pause(1e-5)
        plt.clf()

    def display_move(self, move: Move, show: bool = True):
        """Displays the move on the board via matplotlib

        Args:
            move (Move): move to display
        """
        temp_array = self._get_empty_board()
        for idx_pair in move.idxs:
            row, col = idx_pair
            temp_array[row][col] = 10

        plt.figure()
        plt.imshow(self.array + temp_array, cmap="copper")
        if show:
            plt.title(f"Move for {move.colour}")
            plt.show()

    def display_idxs(self, idxs: list[tuple[int]], on_empty_board: bool = True, show: bool = True):
        """Displays the idxs on the board via matplotlib

        Args:
            idxs (list[tuple[int]]): idxs to display
        """
        if on_empty_board:
            temp_array = self._get_empty_board()
        else:
            temp_array = self.array

        for idx_pair in idxs:
            row, col = idx_pair
            temp_array[row][col] = 1

        plt.figure()
        plt.imshow(temp_array, cmap="copper")
        if show:
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
        # if no moves played yet for colour, use brute force to find allowed moves
        if not any(value == colour.int_id for value in self.flat_array):
            valid_moves = self._find_valid_moves_brute_force(colour)
            self.__valid_moves_dict[colour] = valid_moves

        return self.__valid_moves_dict[colour]

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
                self._validate_overlap,
                self._validate_edge_relation,
                self._validate_corner_relation,
                self._validate_unused_piece,
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

    def check_if_board_corner_idx(self, idx: tuple[int]) -> bool:
        """Checks if the supplied idx is the corner of a board.

        Args:
            idx (tuple[int]): idx to check

        Returns:
            bool: if the supplied idx is a corner
        """
        # checks if an idx is a corner idx.
        return idx in self.corner_idxs
    
    @cache
    def get_diagonal_idxs_from_idx(self, idx: tuple[int, int]) -> list[tuple[int, int]]:
        """Gets the diagonal indices from a given index within bounds."""
        row, col = idx

        # Only include diagonal indices that are within bounds
        diagonal_idxs = [
            (row + dx, col + dy)
            for dx, dy in self.diagonal_offsets
            if self.check_coord_in_board((row + dx, col + dy))
        ]

        return diagonal_idxs

    @cached_property
    def adjacent_offsets(self) -> list[tuple[int, int]]:
        """Cached list of offsets for adjacent indices."""
        return [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    @cached_property
    def diagonal_offsets(self) -> list[tuple[int, int]]:
        """Cached list of offsets for diagonal indices."""
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    @cache
    def get_adjacent_idxs_from_idx(self, idx: tuple[int]) -> list[tuple[int]]:
        """Gets the adjacent idxs from a given index.
        These are +/- 1 for row and column but never both

        Additionally checks that we are in the bounds

        Args:
            idx (tuple[int]): index to check

        Returns:
            list[tuple[int]]: adjacent indices
        """
        # adjacent neighbours are +- 1 in one idx
        row, col = idx
        adjacent_idxs = [
            (row + dx, col + dy)
            for dx, dy in self.adjacent_offsets
            if self.check_coord_in_board((row + dx, col + dy))
        ]
        return adjacent_idxs

    @cache
    def check_coord_in_board(self, coord_pair: tuple[int]) -> bool:
        """Checks that a given coord pair exists within the board.


        Args:
            coord_pair (tuple[int]): coord_pair to check

        Returns:
            bool : if the coord pair is in the board
        """
        return all(0 <= coord <= self.arr_dimension for coord in coord_pair)

    def _update_valid_moves(self):
        """Updates the valid moves for each colour.

        This is done by removing any invalid moves that could have been
        created from the last move, then finding any new valid moves
        that could have been created from the last move.
        """
        self._remove_moves_of_latest_piece()
        self.remove_invalid_moves_based_on_last_move()

        new_valid_moves = self._find_new_valid_moves_from_last_move()
        latest_colour = self.latest_move.colour

        self._add_only_new_moves(new_valid_moves, latest_colour)

    def _remove_moves_of_latest_piece(self):
        """Removes all moves of the latest piece from the valid moves
        for the latest colour
        """
        latest_colour = self.latest_move.colour
        latest_type = self.latest_move.piece_type

        self.__valid_moves_dict[latest_colour] = [
            move for move in self.__valid_moves_dict[latest_colour] if move.piece_type != latest_type
        ]

    def remove_invalid_moves_based_on_last_move(self):
        """Removes all moves that could have been made invalid
        by the last move.
        This could occur due to
        - overlap with previous move

        for moves of the same colour
        - touching sides with the last move

        """

        # check against latest moves idxs
        latest_idxs = self.latest_move.idxs
        
        # for each colour
        # find all the moves could have been affected by the last move
        for colour in BoardStatesEnum.get_player_colours():

            # if its the same colour we also need to check the neighbours
            # as sides cant touch between the same colour
            additional_idxs = []
            if colour == self.latest_move.colour:
                additional_idxs = self._get_neighbouring_idxs_from_idxs(latest_idxs)

            # check all existing valid moves for this colour to see if impaced
            checked_moves = []
            for move in self.__valid_moves_dict[colour]:

                # remove overlaps with the last move
                if any(idx in latest_idxs for idx in move.idxs):
                    continue

                # if doesnt touch any of the idxs its not affected
                if not any(idx in additional_idxs for idx in move.idxs):
                    checked_moves.append(move)
                    continue

                # impacted but still valid
                if self.validate_move(move):
                    checked_moves.append(move)

            self.__valid_moves_dict[colour] = checked_moves


    def _get_neighbouring_idxs_from_idxs(self, idxs: list[tuple[int]]) -> list[tuple[int]]:
        """Gets all the neighbouring idxs from a list of idxs

        Args:
            idxs (list[tuple[int]]): idxs to get neighbours from

        Returns:
            list[tuple[int]]: list of neighbouring idxs
        """
        neighbouring_idxs = []

        for idx in idxs:

            neighbours = self.get_adjacent_idxs_from_idx(idx)

            # remove duplicates
            for neighbour in neighbours:
                if neighbour in neighbouring_idxs:
                    continue
                neighbouring_idxs.append(neighbour)

        return neighbouring_idxs

    def _find_new_valid_moves_from_last_move(self) -> list[Move]:
        """Finds all the new valid moves that could have been created
        from the last move.

        Returns:
            list[Move]: list of new valid moves
        """
        last_move_idxs = self.latest_move.idxs
        colour = self.latest_move.colour

        # find corners of move
        corner_idxs = [idx for idx in last_move_idxs if self._check_if_idx_is_corner_of_colour(idx, colour)]

        origins = []
        for corner in corner_idxs:
            origins += self._get_valid_origins_from_corner(corner, colour)

        valid_moves = self._find_valid_moves_from_origins(colour, origins)

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
        possible_origins = self._get_possible_origins_for_colour(colour)
        valid_moves = self._find_valid_moves_from_origins(colour, possible_origins)
        return valid_moves

    def _find_valid_moves_from_origins(self, colour: BoardStatesEnum, origins: list[tuple[int]]) -> list[Move]:
        """Finds all valid moves for the colour from the supplied origins.

        Args:
            colour (BoardStatesEnum): colour to find moves for
            origins (list[tuple[int]]): origins to find moves from

        Returns:
            list[Move]: list of valid moves
        """
        valid_moves = []
        for origin in origins:
            for piece in self.__piece_sets[colour].pieces:
                for piece_rep in piece.all_idx_representations:

                    # build move from representation
                    move = Move.from_piece_representation(colour, piece.name, piece_rep, origin)

                    # check if the piece can be placed
                    if self.validate_move(move):
                        valid_moves.append(move)

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
        if not any(value == colour.int_id for value in self.flat_array):
            empty_corners = [corner for corner in self.corner_idxs if not self.array[corner[0]][corner[1]]]
            return empty_corners
        
        # get all the corners for the colour
        corner_idxs = self._get_corner_idxs_for_colour(colour)

        # get all the origins for the corners
        origins = []
        for corner in corner_idxs:

            new_origins = self._get_valid_origins_from_corner(corner, colour)

            for origin in new_origins:
                if origin in origins:
                    continue
                origins.append(origin)

        return origins

    def _get_valid_origins_from_corner(self, corner: tuple[int], colour: BoardStatesEnum) -> list[tuple[int]]:
        """Returns all valid origins from a corner.
        This is all the diagonals from the corner

        Args:
            corner (tuple[int]): corner to get origins from

        Returns:
            list[tuple[int]]: list of all valid origins
        """
        # get all the diagonals from the corner
        possible_origins = self.get_diagonal_idxs_from_idx(corner)
        valid_origins = []

        for origin in possible_origins:
            # remove any that are already populated
            if self.array[origin[0]][origin[1]]:
                continue

            # get the adjacent neighbours
            adjacent_neighbours = self.get_adjacent_idxs_from_idx(origin)

            # check if any of the neighbours are the same colour
            if any(self.array[neighbour[0]][neighbour[1]] == colour.int_id for neighbour in adjacent_neighbours):
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
        for row in range(self.dimension):
            for col in range(self.dimension):

                if not self._check_if_idx_is_corner_of_colour((row, col), colour):
                    continue

                corner_idxs.append((row, col))

        return corner_idxs

    def _check_if_idx_is_corner_of_colour(self, idx: tuple[int], colour: BoardStatesEnum) -> bool:
        """Checks if the supplied idx is a corner of a piece of the colour

        Args:
            idx (tuple[int]): idx to check
            colour (BoardStatesEnum): colour to check

        Returns:
            bool: if the idx is a corner of the colour
        """
        row, col = idx
        # if the cell is not the colour, skip
        if not self.array[row][col] == colour.int_id:
            return False
        
        # find the horizontal and vertical neighbours
        vertical_neighbours = [(row, col - 1), (row, col + 1)]
        vertical_neighbours = [idx for idx in vertical_neighbours if self.check_coord_in_board(idx)]
        horizontal_neighbours = [(row - 1, col), (row + 1, col)]
        horizontal_neighbours = [idx for idx in horizontal_neighbours if self.check_coord_in_board(idx)]

        # find neightbour count of colour
        horizonal_score = sum([self.array[_row][_col] == colour.int_id for _row, _col in horizontal_neighbours])
        vertical_score = sum([self.array[_row][_col] == colour.int_id for _row, _col in vertical_neighbours])

        # account for game borders
        if row in [0, self.arr_dimension]:
            horizonal_score += 1
        if col in [0, self.arr_dimension]:
            vertical_score += 1

        # corner has only 1 neighbour in vertical or horizontal
        if horizonal_score > 1 or vertical_score > 1:
            return False
        
        return True

    def _validate_piece_idx_matches_type(self, move: Move):
        """Validates that the idx of the move match the topology of the piece
        in the move

        Args:
            move (Move): move to check

        Raises:
            InvalidMove: if the move idxs to match the move piece type
        """
        # check if the idx matches the shape

        piece = self.__piece_sets[move.colour].get_piece_by_name(move.piece_type)

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
        if move.piece_type in self.__piece_sets[move.colour].present_types:
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
            if self.check_if_board_corner_idx(idx):
                return
            diagonal_neighbours = self.get_diagonal_idxs_from_idx(idx)
            for diagonal_neighbour in diagonal_neighbours:
                row, col = diagonal_neighbour
                # check if corner relation obeyed
                if self.array[row][col] == move.colour.int_id:
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
            # Get adjacent neighbors
            for row, col in self.get_adjacent_idxs_from_idx(idx):
                # Check if the adjacent cell has the same color ID
                if self.array[row][col] == move.colour.int_id:
                    raise InvalidMove(f"The move does not obey the side relation, {move}")

    def _validate_in_bounds(self, move: Move):
        """Checks that the move is fully contained within the board

        Args:
            move (Move): move to check

        Raises:
            InvalidMove: if the move does not fit within the board
        """
        for idx in move.idxs:
            if not self.check_coord_in_board(idx):
                raise InvalidMove(f"Move does not fit in the board, {move}")
    

    def _get_initial_piece_dict(self) -> dict[BoardStatesEnum, PieceSet]:
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

    def _add_only_new_moves(self, new_valid_moves: list[Move], colour: BoardStatesEnum):
        """Adds only the unique new valid moves to the valid moves dict

        Args:
            new_valid_moves (list[Move]): new valid moves
            colour (BoardStatesEnum): colour to add the moves to
        """
        rep_nums = [self._convert_move_to_str_representation(move) for move in self.__valid_moves_dict[colour]]
        for move in new_valid_moves:
            rep_num = self._convert_move_to_str_representation(move)
            if rep_num in rep_nums:
                continue
            self.__valid_moves_dict[colour].append(move)

    def _convert_move_to_str_representation(self, move: Move) -> str:
        """Converts a move to a int representation by joining the idxs into
        a single int

        Args:
            move (Move): move to convert

        Returns:
            int: int representation
        """
        return "".join([str(idx[0]) + str(idx[1]) for idx in move.idxs])

    @property
    def array(self) -> np.ndarray:
        """Returns the state of the board as a nxn interger array,
        the ints map to the colours via the BoardStatesEnum.

        Returns:
            np.ndarray: current state of the board
        """
        return self.__array
    
    @property
    def piece_sets(self) -> dict[BoardStatesEnum, PieceSet]:
        """Returns the piece sets for each colour

        Returns:
            dict[BoardStatesEnum, PieceSet]: piece sets for each colour
        """
        return self.__piece_sets

    @property
    def flat_array(self) -> np.ndarray:
        """Returns the state of the board as a flat array

        Returns:
            np.ndarray: flat array of the board
        """
        return self.array.flatten()

    @property
    def latest_move(self) -> Move:
        """Returns the latest move played on the board

        Returns:
            Move: latest move
        """
        return self.__latest_move

    @property
    def valid_moves_dict(self) -> dict[BoardStatesEnum, list[Move]]:
        """Returns the valid moves for each colour

        Returns:
            dict[BoardStatesEnum, list[Move]]: valid moves for each colour
        """
        return self.__valid_moves_dict

    @cached_property
    def dimension(self) -> int:
        """returns the dimension of the board,
        the board is nxn where is is the dimension

        Returns:
            int: dimensino of the board
        """
        return self.__dimension

    @cached_property
    def arr_dimension(self) -> int:
        """Returns the dimension of the array

        Returns:
            int: dimension of the array
        """
        return self.__dimension - 1

    @cached_property
    def corner_idxs(self) -> list[tuple[int]]:
        """Returns the corner idxs of the board.

        Returns:
            list[tuple[int]]: corner idxs
        """
        corner_idxs = [
            (0, 0),
            (0, self.arr_dimension),
            (self.arr_dimension, 0),
            (self.arr_dimension, self.arr_dimension),
        ]
        return corner_idxs
    
    @property
    def move_list(self) -> list[Move]:
        """Returns all the moves played in the game
        """
        return self.__move_list
    
    @property
    def centre_idx(self) -> tuple[int]:
        """Returns the centre idx of the board

        Returns:
            tuple[int]: centre idx
        """
        return (self.dimension//2,self.dimension//2)
    
    def idx_pair_occupied(self,idx_pair: tuple[int,int]):
        row, col = idx_pair
        return self.array[row][col]
    
    def get_moves_since_last_turn(self,colour:BoardStatesEnum):
        """Finds the moves played since the last turn of the supplied colour"""
        moves_played = []

        for move in self.__move_list[::-1]:
            
            if move.colour == colour:
                break
            
            moves_played.append()

        return moves_played 
    
    def get_distance_from_center(self, move: Move):
        distances = []
        for idx in move.idxs:
            distance = ((self.centre_idx[0]-idx[0])**2 + (self.centre_idx[1]-idx[1])**2)**0.5
            distances.append(distance)
        return min(distances)

