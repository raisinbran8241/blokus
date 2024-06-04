from piece import Piece
from copy import deepcopy


class Player:
    """Represents a Blokus player. Can do a bunch of fancy stuff with pieces"""

    def __init__(self, name: str, player_id: int):
        self._name = name
        self._id = player_id
        self._pieces: list[Piece] = [Piece([[]], 0)]  # Default starts with empty
        self._piece_id: int = 0

        self._pieces.append(Piece([[0]], 1))  # 1-I (1)
        self._pieces.append(Piece([[0, 0]], 2))  # 2-I (2)
        self._pieces.append(Piece([[0, 0, 0]], 3))  # 3-L (3)
        self._pieces.append(Piece([[-1, 0], [0, 0]], 4))  # 3-I (4)

        # Tetrominoes
        self._pieces.append(Piece([[-1, 0], [0, 0], [0, -1]], 5))  # 4-S (5)
        self._pieces.append(Piece([[0, 0], [0, 0]], 6))  # 4-O (6)
        self._pieces.append(Piece([[-1, 0, -1], [0, 0, 0]], 7))  # 4-T (7)
        self._pieces.append(Piece([[0, 0, 0], [-1, -1, 0]], 8))  # 4-L (8)
        self._pieces.append(Piece([[0, 0, 0, 0]], 9))  # 4-I (9)

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

        self._pieces_copy = deepcopy(self._pieces)
        self._available_pieces = [_ for _ in range(1, 22)]
        self._squares_left = 89
        self._all_pieces_used = False

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

    @property
    def pieces_copy(self):
        return self._pieces_copy

    @property
    def available_pieces(self):
        return self._available_pieces

    @property
    def squares_left(self):
        return self._squares_left

    @property
    def all_pieces_used(self):
        return self._all_pieces_used

    def get_piece(self) -> Piece:
        """Gets the selected piece of the player."""
        if self._piece_id in self._available_pieces:
            return self._pieces[
                self._piece_id
            ]  # Don't return copy piece because it doesn't keep the orientation
        else:
            return self._pieces[0]

    def set_to_lowest_value_piece(self) -> None:
        """Sets the piece_id to whichever piece has the lowest ID."""
        for i in range(1, 22):
            if i in self._available_pieces:
                self._piece_id = i
                break

    def use_piece(self) -> None:
        self._available_pieces.remove(self._piece_id)
        self._squares_left -= self._pieces[self._piece_id].get_num_squares()

        if len(self._available_pieces) == 0:
            self._all_pieces_used = True

        self.set_to_lowest_value_piece()

    def left_piece(self) -> None:
        if not (self._piece_id - 1) % 5 == 0 and self.piece_id > 1:
            self._piece_id -= 1

    def right_piece(self) -> None:
        if not self._piece_id % 5 == 0 and self.piece_id != 21:
            self._piece_id += 1

    def up_piece(self) -> None:
        if not self._piece_id - 5 <= 0:
            self._piece_id -= 5

    def down_piece(self) -> None:
        if not self._piece_id + 5 >= 22:
            self._piece_id += 5
