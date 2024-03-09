from typing import List

from piece import Piece


class Player:
    """Represents a Blokus player. Can do a bunch of fancy stuff with pieces"""

    def __init__(self, name: str, player_id: int):
        self._name = name
        self._id = player_id
        self._pieces: List[Piece] = [Piece([[]])]  # Default starts with empty
        self._selected_piece_id: int = 0

        # Shove pieces into init (might change later)
        self._pieces.append(Piece([[0]]))  # 1-I (1)
        self._pieces.append(Piece([[0, 0]]))  # 2-I (2)
        self._pieces.append(Piece([[0, 0, 0]]))  # 3-L (3)
        self._pieces.append(Piece([[-1, 0], [0, 0]]))  # 3-I (4)

        # Tetrominoes
        self._pieces.append(Piece([[-1, 0], [0, 0], [0, -1]]))  # 4-S (5)
        self._pieces.append(Piece([[0, 0], [0, 0]]))  # 4-O (6)
        self._pieces.append(Piece([[-1, 0, -1], [0, 0, 0]]))  # 4-T (7)
        self._pieces.append(Piece([[0, 0, 0], [-1, -1, 0]]))  # 4-L (8)
        self._pieces.append(Piece([[0, 0, 0, 0, 0]]))  # 4-I (9)

        # Pentominoes
        self._pieces.append(Piece([[-1, 0], [0, 0], [0, 0]]))  # 5-P (10)
        self._pieces.append(Piece([[0, 0], [0, -1], [0, 0]]))  # 5-U (11)
        self._pieces.append(Piece([[-1, -1, 0], [0, 0, 0], [-1, -1, 0]]))  # 5-T (12)
        self._pieces.append(
            Piece(
                [
                    [-1, 0],
                    [-1, 0],
                    [-1, 0],
                    [0, 0],
                    [0, -1],
                ]
            )  # 5-S (13)
        )
        self._pieces.append(Piece([[-1, 0, 0], [-1, 0, -1], [0, 0, -1]]))  # 5-Z (14)
        self._pieces.append(Piece([[-1, 0, -1], [-1, 0, 0], [0, 0, -1]]))  # 5-F (15)
        self._pieces.append(Piece([[0, 0, 0, 0], [-1, -1, -1, 0]]))  # 5-L (16)
        self._pieces.append(Piece([[-1, 0, 0], [0, 0, -1], [0, -1, -1]]))  # 5-W (17)
        self._pieces.append(Piece([[-1, 0, -1], [0, 0, 0], [-1, 0, -1]]))  # 5-X (18)
        self._pieces.append(Piece([[0, 0, 0, 0, 0]]))  # 5-I (19)
        self._pieces.append(Piece([[-1, -1, 0], [-1, -1, 0], [0, 0, 0]]))  # 5-V (20)
        self._pieces.append(Piece([[-1, 0, -1, -1], [0, 0, 0, 0]]))  # 5-Y (21)

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def pieces(self):
        return self._pieces

    @property
    def selected_piece_id(self):
        return self._selected_piece_id

    @selected_piece_id.setter
    def selected_piece_id(self, piece_id):
        self._selected_piece_id = piece_id

    def get_piece_from_id(self, piece_id):
        return self.pieces[piece_id]
