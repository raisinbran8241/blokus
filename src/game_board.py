from piece import Piece
from typing import List


class GameBoard:
    """Represents the game board and all of its game squares."""

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = [[-1 for _ in range(width)] for _ in range(height)]
        self._first_move = True

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def board(self):
        return self._board

    @property
    def first_move(self):
        return self._first_move

    def place_piece(self, piece: Piece, row: int, col: int, player_id: int) -> bool:
        """Places a piece on the board."""
        # Check if the placement of the piece is valid
        if self.is_placement_valid(piece, row, col, player_id):
            piece_height, piece_width = len(piece), len(piece[0])
            # Loop through and change the board accordingly
            for i in range(piece_height):
                for j in range(piece_width):
                    if piece[i][j] == 0:
                        print(row + i, col + j, player_id)
                        self._board[row + i][col + j] = player_id
            return True
        return False

    def is_placement_valid(
        self, piece: Piece, row: int, col: int, player_id: int
    ) -> bool:
        """Checks if the placement of a piece is valid."""
        # Check if the piece fits within the board
        piece_height, piece_width = len(piece), len(piece[0])
        if (col + piece_width > self._width) or (row + piece_height > self._height):
            return False

        # If it's the first move, then it has to be at a corner
        if self._first_move:
            if player_id == 0:  # Blue, top right
                if row != 0 or col + piece_width != 20 or piece[0][-1] != 0:
                    return False
            elif player_id == 1:  # Yellow, bottom right
                if (
                    row + piece_height != 20
                    or col + piece_width != 20
                    or piece[-1][-1] != 1
                ):
                    return False
            elif player_id == 2:  # Red, bottom left
                if row + piece_height != 20 or col != 0 or piece[-1][0] != 2:
                    return False
            elif player_id == 3:  # Green, top left
                if row != 0 or col != 0 or piece[0][0] != 3:
                    return False
            return True

        touches_corners = False
        for i in range(piece_height):
            for j in range(piece_width):
                if piece[i][j] != -1:
                    # Check that the piece does not overlap with other pieces
                    if self._board[row + i][col + j] != -1:
                        return False

                    # Check if the piece touches sides with another piece of the same player
                    if (
                        row + i + 1 < self._height
                        and self._board[row + i + 1][col + j] == player_id
                    ):  # Bottom
                        return False
                    if (
                        row + i - 1 > 0
                        and self._board[row + i - 1][col + j] == player_id
                    ):  # Top
                        return False
                    if (
                        col + j + 1 < self._width
                        and self._board[row + i][col + j + 1] == player_id
                    ):  # Right
                        return False
                    if (
                        col + j - 1 > 0
                        and self._board[row + i][col + j - 1] == player_id
                    ):  # Left
                        return False

                    # Check if the piece touches corners with another piece of the same player
                    if (  # Bottom-right corner
                        row + i + 1 < self._height
                        and col + j + 1 < self._width
                        and self._board[row + i + 1][col + j + 1] == player_id
                    ):
                        touches_corners = True
                    if (  # Bottom-left corner
                        row + i + 1 < self._height
                        and col + j - 1 > 0
                        and self._board[row + i + 1][col + j - 1] == player_id
                    ):
                        touches_corners = True
                    if (  # Top-left corner
                        row + i - 1 > 0
                        and col + j - 1 > 0
                        and self._board[row + i - 1][col + j - 1] == player_id
                    ):
                        touches_corners = True
                    if (  # Top-right corner
                        row + i - 1 > 0
                        and col + j + 1 < self._width
                        and self._board[row + i - 1][col + j + 1] == player_id
                    ):
                        touches_corners = True

        if touches_corners:
            return True
        return False
