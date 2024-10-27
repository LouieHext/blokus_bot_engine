# Python imports
import random

from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.move import Move

# Internal imports
from blokus.player.base_player import BasePlayer


class CornerBot(BasePlayer):
    """This bot plays to maximise the number of potential corners
    if multiple moves are equal will pick the largest
    """
    def __init__(self, board: Board, colour: BoardStatesEnum):
        # call super constructor
        super().__init__(board,colour)
       
        self._move_to_origin_idx_map = {}

    def select_best_move(self, moves: list[Move]) -> Move:
        """Selects a random move

        Args:
            moves (list[Move]): moves to select from

        Returns:
            Move: randomly selected move
        """
        self._update_origin_dict(moves)

        # return the move that has the most potential new origins
        random.shuffle(moves)
        best_move = max(moves, key=self._get_score_for_move)
        return best_move
    
    def _get_score_for_move(self, move: Move):
        num_origings = len(self._move_to_origin_idx_map[move])
        size_of_move = len(move.idxs)
        distance_from_center = self._get_distance_from_center(move)
        location_multiplier = 1 - (distance_from_center/self.board.dimension)**2
        span_of_move = self._calculate_span_of_move(move)
        span_multiplier = 1 + (span_of_move/10)**0.5
        return (num_origings + size_of_move) * location_multiplier * span_multiplier 
    
    def _update_origin_dict(self, moves: list[Move]):
        # remove any stored infomation from now invalid moves
        self._tidy_up_dictionaries(moves)


        # check if latest moves impacted current valid moves
        for move in moves:
            # move is new, calculate its corner score
            if move not in self._move_to_origin_idx_map:
                self._calculate_new_origings_for_move(move)
                continue

            # move has been seen before, update its score
            self._update_origings_for_move(move)

        
    def _tidy_up_dictionaries(self,moves: list[Move]):
        # remove any keys that are not in the moves list
        keys_to_remove = [key for key in self._move_to_origin_idx_map if key not in moves]
        for key in keys_to_remove:
            del self._move_to_origin_idx_map[key]

    def _update_origings_for_move(self, move: Move):
        self._move_to_origin_idx_map[move] = [idx_pair for idx_pair in self._move_to_origin_idx_map[move] if not self.board.idx_pair_occupied(idx_pair)]


    def _calculate_new_origings_for_move(self,move: Move):
        # find corners of move piece
        future_board = self.board.create_future_board_from_move(move)
        
        corners_of_move = [idx_pair for idx_pair in move.idxs if future_board._check_if_idx_is_corner_of_colour(idx_pair,self.colour)]
        # find potential origins for new moves
        origins_of_move = []
        for corner in corners_of_move:
            origins_of_move += future_board._get_valid_origins_from_corner(corner, self.colour)
        origins_of_move = list(set(origins_of_move))
        
        # update ofigin map
        self._move_to_origin_idx_map[move] = origins_of_move

    def _get_distance_from_center(self, move: Move):
        center = (self.board.dimension//2,self.board.dimension//2)
        distances = []
        for idx in move.idxs:
            distance = ((center[0]-idx[0])**2 + (center[1]-idx[1])**2)**0.5
            distances.append(distance)
        return min(distances)


    def _calculate_span_of_move(self, move: Move):
        x_coords = [idx[0] for idx in move.idxs]
        y_coords = [idx[1] for idx in move.idxs]
        return max(x_coords) - min(x_coords) + max(y_coords) - min(y_coords)   
    