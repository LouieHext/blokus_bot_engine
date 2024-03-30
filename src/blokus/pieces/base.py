#Python Imports
#External Imports
import numpy as np

#Internal Imports
from blokus.pieces.piece_names import PieceNameEnum


class BasePiece():
    def __init__(self,base_binary_repr: np.ndarray, name:PieceNameEnum):
        self.base_binary_repr = base_binary_repr
        self.all_idx_representations = self.generate_all_variants_from_base()
        self.name = name
    
    @property
    def size(self)-> int:
        """Returns the size of the piece,
        which is how many squares it occupies

        Returns:
            int: size of the piece
        """
        return np.sum(self.base_binary_repr)

    def generate_all_variants_from_base(self):
        """
        Generates all the possible variations of a piece in terms
        of indexes. 

        For a piece of max dimension N, it can be represented as an array
        with dimensions 2N-1 x 2N-1. This is because the piece can be rotated
        and mirrored. 
        This function generates all the possible variations of the piece

        Returns:
            list[list[tuple[int]]]: list of all the possible variations of the piece
        """
         # get the 4 rotations
        rotations = self._get_rotations_of_piece()
        # for each rotation get the mirror also
        all_rotations = []
        for rotation in rotations:
            all_rotations.append(rotation)
            all_rotations.append(self._get_flip_of_binary_repr(rotation))
        # remove duplicates
        unqiue_rotations = self._remove_duplicate_binary_reprs(all_rotations)
        # convert to list of indexes
        all_idx_variations = [self._convert_binary_repr_to_idx(rotation) for rotation in unqiue_rotations]
        return all_idx_variations


    def _get_rotations_of_binary_repr(self,binary_repr: np.ndarray) -> list[np.ndarray]:
        """Generates all the rotations of a binary representation,
        the rotations are 90 degrees from each other

        Args:
            binary_repr (np.ndarray): binary representation of the piece

        Returns:
            list[np.ndarray]: list of all rotations
        """
        rotations = [binary_repr]
        for _ in range(3):
            rotations.append(np.rot90(rotations[-1]))
        return rotations
    
    def _get_flip_of_binary_repr(self,binary_repr: np.ndarray) -> np.ndarray:
        """Generates the mirror of a binary representation

        Args:
            binary_repr (np.ndarray): binary representation of the piece

        Returns:
            np.ndarray: mirror of the binary representation
        """
        return np.fliplr(binary_repr)

    def _remove_duplicate_binary_reprs(self,all_variations: list[np.ndarray]) -> list[np.ndarray]:
        """Removes duplicate binary representations from a list

        Args:
            all_variations (list[np.ndarray]): list of binary representations

        Returns:
            list[np.ndarray]: list of binary representations with duplicates removed
        """
        unique_variations = []
        for variation in all_variations:
            if any(np.array_equal(variation, unique) for unique in unique_variations):
                continue
            unique_variations.append(variation)
        return unique_variations
    
    def _convert_binary_repr_to_idx(self,binary_repr: np.ndarray) -> list[tuple[int]]:
        """Converts a binary representation to a list of active indexes.
        The active indexes are the indexes where the binary representation
        is 1.
        We also shift the indexes so the middle of the piece is at 0,0

        Args:
            binary_repr (np.ndarray): binary representation of the piece

        Returns:
            list[tuple[int]]: list of indexes
        """
        shift_amt = binary_repr.shape[0] // 2
        idxs = np.argwhere(binary_repr == 1)
        # shift idxs so the middle is at 0,0
        idxs -= shift_amt
        return idxs

