from typing import List

from piece import Piece


class Player:
    """Represents a Blokus player. Can do a bunch of fancy stuff with pieces"""

    def __init__(self, name: str, player_id: int):
        self._name = name
        self._id = player_id
        self._pieces: List[Piece] = [Piece([[]], 0)]  # Default starts with empty
        self._piece_id: int = 0

        # Shove pieces into init (might change later)
        self._pieces.append(Piece([[0]], 1))  # 1-I (1)
        self._pieces.append(Piece([[0, 0]], 2))  # 2-I (2)
        self._pieces.append(Piece([[0, 0, 0]], 3))  # 3-L (3)
        self._pieces.append(Piece([[-1, 0], [0, 0]], 4))  # 3-I (4)

        # Tetrominoes
        self._pieces.append(Piece([[-1, 0], [0, 0], [0, -1]], 5))  # 4-S (5)
        self._pieces.append(Piece([[0, 0], [0, 0]], 6))  # 4-O (6)
        self._pieces.append(Piece([[-1, 0, -1], [0, 0, 0]], 7))  # 4-T (7)
        self._pieces.append(Piece([[0, 0, 0], [-1, -1, 0]], 8))  # 4-L (8)
        self._pieces.append(Piece([[0, 0, 0, 0, 0]], 9))  # 4-I (9)

        # Pentominoes
        self._pieces.append(Piece([[-1, 0], [0, 0], [0, 0]], 10))  # 5-P (10)
        self._pieces.append(Piece([[0, 0], [0, -1], [0, 0]], 11))  # 5-U (11)
        self._pieces.append(
            Piece([[-1, -1, 0], [0, 0, 0], [-1, -1, 0]], 12)
        )  # 5-T (12)
        self._pieces.append(
            Piece(
                [
                    [-1, 0],
                    [-1, 0],
                    [0, 0],
                    [0, -1],
                ],
                13,
            )  # 5-S (13)
        )
        self._pieces.append(
            Piece([[-1, 0, 0], [-1, 0, -1], [0, 0, -1]], 14)
        )  # 5-Z (14)
        self._pieces.append(
            Piece([[-1, 0, -1], [-1, 0, 0], [0, 0, -1]], 15)
        )  # 5-F (15)
        self._pieces.append(Piece([[0, 0, 0, 0], [-1, -1, -1, 0]], 16))  # 5-L (16)
        self._pieces.append(
            Piece([[-1, 0, 0], [0, 0, -1], [0, -1, -1]], 17)
        )  # 5-W (17)
        self._pieces.append(
            Piece([[-1, 0, -1], [0, 0, 0], [-1, 0, -1]], 18)
        )  # 5-X (18)
        self._pieces.append(Piece([[0, 0, 0, 0, 0]], 19))  # 5-I (19)
        self._pieces.append(
            Piece([[-1, -1, 0], [-1, -1, 0], [0, 0, 0]], 20)
        )  # 5-V (20)
        self._pieces.append(Piece([[-1, 0, -1, -1], [0, 0, 0, 0]], 21))  # 5-Y (21)

        self._available_pieces = [_ for _ in range(1, 22)]

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def used_pieces(self):
        return self._available_pieces

    @property
    def piece_id(self):
        return self._piece_id

    @piece_id.setter
    def piece_id(self, piece_id) -> None:
        """Sets the selected piece of the player."""
        if piece_id in self._available_pieces:
            self._piece_id = piece_id
        else:
            pass  # TODO: Raise

    def get_piece(self) -> Piece:
        """Gets the selected piece of the player."""
        return self._pieces[self._piece_id]

    def get_piece_from_id(self, piece_id) -> Piece:
        """Returns a piece from its ID."""
        return self._pieces[piece_id]

    def use_piece(self) -> None:
        if self._piece_id in self._available_pieces:
            self._available_pieces.remove(self._piece_id)
        else:
            pass  # TODO: Raise an error

    def next_piece(self) -> None:
        self._piece_id = self._available_pieces[
            (self.piece_id) % len(self._available_pieces)
        ]  # Already added one (one-index)

    def previous_piece(self) -> None:
        self._piece_id = self._available_pieces[
            self.piece_id - 1 - 1
        ]  # One for one-index, one for -1
