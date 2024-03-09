from typing import List


class Piece:
    def __init__(self, shape: List[List[int]]):
        self._shape = shape
        self._orientation = 0  # 0: normal, 1: (clockwise) 90, 180, 270
        self._mirror = 0  # 0: normal, 1: vertical, 2: horizontal

    def __str__(self):
        return str(self._shape)

    def __len__(self):
        return len(self.shape)

    def __getitem__(self, idx):
        return self.shape[idx]

    def rotate_clockwise(self):
        """Rotates the piece clockwise."""
        self.shape = [list(elem) for elem in list(zip(*self.shape[::-1]))]
        self.orientation += 1

    def rotate_counterclockwise(self):
        """Rotates the piece counterclockwise."""
        self.shape = [list(elem) for elem in list(zip(*self.shape))[::-1]]
        self.orientation -= 1

    def flip_vertically(self):
        """Flips the piece vertically."""
        # Flip piece vertically by appending from last to first row
        self.shape = [self.shape[i] for i in range(len(self.shape) - 1, -1, -1)]
        self.mirror += 1

    def flip_horizontally(self):
        """Flips the piece horizontally."""
        # Flip piece horizontally by reversing every row
        self._shape = [list(reversed(elem)) for elem in self.shape]
        self.mirror += 2

    @property
    def shape(self):
        return self._shape

    @property
    def orientation(self):
        return self._orientation

    @property
    def mirror(self):
        return self._mirror

    @shape.setter
    def shape(self, value):
        self._shape = value

    @orientation.setter
    def orientation(self, value):
        """The orientation value of the piece. Clockwise adds, counterclockwise subtracts"""
        self._orientation = value % 4

    @mirror.setter
    def mirror(self, value):
        """
        Sets the mirror value of the piece. The values represent:
        0: original
        1: vertical
        2: horizontally
        """
        # Piece is being flipped vertically
        if value == self.mirror + 1:
            if self.mirror == 1:
                self._mirror = 0
            # Mirrored horizontally + vertical is equal to rotated 180 degrees
            elif self.mirror == 2:
                self._mirror = 0
                self.orientation += 2
            else:
                self._mirror = 1
        # Piece is being flipped horizontally
        elif value == self.mirror + 2:
            if self.mirror == 2:
                self._mirror = 0
            elif self.mirror == 1:
                self.mirror = 0
                self.orientation += 2
            else:
                self._mirror = 2
