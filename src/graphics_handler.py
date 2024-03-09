import pygame
from game_board import GameBoard


class GraphicsHandler:
    """Handles the graphical aspects of the game, such as drawing and updating the board and pieces."""

    def __init__(self):
        # Set up the graphical environment
        pygame.init()
        self._screen = pygame.display.set_mode((1200, 750))
        self._screen.fill((160, 160, 160))
        pygame.display.set_caption("Blokus")

        self._player_colors = [
            (1, 90, 169),
            (253, 184, 15),
            (214, 29, 36),
            (0, 161, 74),
        ]

        # Drawing all the squares (20x20)
        self._coordinates = []
        for i in range(21):
            self._coordinates.append(i * 30 + i)

        # The extra 290 for the row, 65 for the col is for centering
        line_color = (76, 76, 76)
        for i in range(21):  # Draw columns
            pygame.draw.line(
                self._screen,
                line_color,
                (self._coordinates[i] + 290, 0 + 65),
                (self._coordinates[i] + 290, self._coordinates[-1] + 65),
            )
        for i in range(21):  # Draw rows
            pygame.draw.line(
                self._screen,
                line_color,
                (0 + 290, self._coordinates[i] + 65),
                (self._coordinates[-1] + 290, self._coordinates[i] + 65),
            )

    def update_screen(self, game_board: GameBoard):
        """Updates the squares based on the state of the board."""
        for row in range(game_board.height):
            for col in range(game_board.width):
                color = game_board.board[row][col]
                if color >= 0:
                    pygame.draw.rect(
                        self._screen,
                        self._player_colors[color],
                        (
                            self._coordinates[col] + 291,
                            self._coordinates[row] + 66,
                            30,
                            30,
                        ),
                    )
