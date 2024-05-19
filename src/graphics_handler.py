import pygame
from game_board import GameBoard


class GraphicsHandler:
    """Handles the graphical aspects of the game, such as drawing and updating the board and pieces."""

    def __init__(self):
        # Set up the graphical environment
        self._screen = pygame.display.set_mode((1400, 750))
        self._BG_COLOR = (160, 160, 160)
        self._X_MARGIN = 440
        self._Y_MARGIN = 160
        self.font = pygame.font.SysFont("Fira Code", 30)
        text_surface = self.font.render("'s turn", False, (0, 0, 0))

        self._screen.fill(self._BG_COLOR)
        self._screen.blit(text_surface, (700, 70))
        pygame.display.set_caption("Blokus")

        self._player_colors = [
            (1, 90, 169),
            (253, 184, 15),
            (214, 29, 36),
            (0, 161, 74),
            (100, 100, 100),
        ]

        # Drawing all the squares (20x20)
        self._coordinates = []
        for i in range(21):
            self._coordinates.append(i * 25 + i)

        line_color = (76, 76, 76)
        for i in range(21):  # Draw columns
            pygame.draw.line(
                self._screen,
                line_color,
                (self._coordinates[i] + self._X_MARGIN, 0 + self._Y_MARGIN),
                (
                    self._coordinates[i] + self._X_MARGIN,
                    self._coordinates[-1] + self._Y_MARGIN,
                ),
            )
        for i in range(21):  # Draw rows
            pygame.draw.line(
                self._screen,
                line_color,
                (0 + self._X_MARGIN, self._coordinates[i] + self._Y_MARGIN),
                (
                    self._coordinates[-1] + self._X_MARGIN,
                    self._coordinates[i] + self._Y_MARGIN,
                ),
            )

    def update_screen(self, game_board: GameBoard, current_player: int) -> None:
        """Updates the squares based on the state of the board."""

        pygame.draw.rect(
            self._screen, self._player_colors[current_player], (670, 70, 30, 30)
        )

        for row in range(game_board.height):
            for col in range(game_board.width):
                color = game_board.shadow_board[row][col]
                if color >= 0:
                    pygame.draw.rect(
                        self._screen,
                        self._player_colors[color],
                        (
                            self._coordinates[col] + self._X_MARGIN + 1,
                            self._coordinates[row] + self._Y_MARGIN + 1,
                            25,
                            25,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self._screen,
                        self._BG_COLOR,
                        (
                            self._coordinates[col] + self._X_MARGIN + 1,
                            self._coordinates[row] + self._Y_MARGIN + 1,
                            25,
                            25,
                        ),
                    )

    def get_square_from_coords(self, coords):
        """Takes a set of coordinates and returns the position on the game board."""
        x = coords[0]
        y = coords[1]
        square = [-1, -1]
        for i in range(len(self._coordinates) - 1):
            val = self._coordinates[i]
            if val <= x - self._X_MARGIN <= val + 25:
                square[1] = i
            if val <= y - self._Y_MARGIN <= val + 25:
                square[0] = i
        return square
