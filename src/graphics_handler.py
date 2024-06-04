import pygame
from game_board import GameBoard
from player import Player


class GraphicsHandler:
    """Handles the graphical aspects of the game, such as drawing and updating the board and pieces."""

    def __init__(self):
        # Set up the graphical environment
        self._screen = pygame.display.set_mode((1400, 750))
        self._BG_COLOR = (160, 160, 160)
        self._X_MARGIN = 440
        self._Y_MARGIN = 160
        self._GRID_BOX_SIZE = 25
        self._PLAYER_GRID_HEIGHT = 65
        self._PLAYER_GRID_WIDTH = 80
        self._PLAYER_GRID_BOX_SIZE = 15

        # Only turn tracker has bigger size font, everything else is 20
        self._FONT_SIZE = 30
        self.font = pygame.font.SysFont("Fira Code", self._FONT_SIZE)
        text_surface = self.font.render("'s turn", False, (0, 0, 0))

        self._FONT_SIZE = 20
        self.font = pygame.font.SysFont("Fira Code", self._FONT_SIZE)

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
        self._LINE_COLOR = (76, 76, 76)

        # Drawing the grid squares (20x20)
        self._coordinates = []
        for i in range(21):
            self._coordinates.append(i * self._GRID_BOX_SIZE + i)
        self._draw_game_grid()

        # Draw player grids (5x4, 4 players)
        self._piece_coordinates_x = []
        self._piece_coordinates_y = []
        for i in range(6):
            self._piece_coordinates_x.append(i * self._PLAYER_GRID_WIDTH + i)
        for i in range(6):
            self._piece_coordinates_y.append(i * self._PLAYER_GRID_HEIGHT + i)

        self._player_grid_margins = [(984, 30), (984, 394), (15, 394), (15, 30)]
        for i in range(len(self._player_grid_margins)):
            self._draw_player_grid(i)

    def update_screen(
        self, game_board: GameBoard, current_player: int, players: list[Player]
    ) -> None:
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
                            self._GRID_BOX_SIZE,
                            self._GRID_BOX_SIZE,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self._screen,
                        self._BG_COLOR,
                        (
                            self._coordinates[col] + self._X_MARGIN + 1,
                            self._coordinates[row] + self._Y_MARGIN + 1,
                            self._GRID_BOX_SIZE,
                            self._GRID_BOX_SIZE,
                        ),
                    )

        for i in range(len(players)):
            self._draw_player_grid_pieces(i, players)
            self._update_score_text(i, players)

    def get_square_from_coords(self, coords):
        """Takes a set of coordinates and returns the position on the game board."""
        x = coords[0]
        y = coords[1]
        square = [-1, -1]
        for i in range(len(self._coordinates) - 1):
            val = self._coordinates[i]
            if val <= x - self._X_MARGIN <= val + self._GRID_BOX_SIZE:
                square[1] = i
            if val <= y - self._Y_MARGIN <= val + self._GRID_BOX_SIZE:
                square[0] = i
        return square

    def _draw_game_grid(self):
        """Draws the main 20x20 grid of the game."""
        for i in range(21):  # Draw columns
            pygame.draw.line(
                self._screen,
                self._LINE_COLOR,
                (self._coordinates[i] + self._X_MARGIN, 0 + self._Y_MARGIN),
                (
                    self._coordinates[i] + self._X_MARGIN,
                    self._coordinates[-1] + self._Y_MARGIN,
                ),
            )
        for i in range(21):  # Draw rows
            pygame.draw.line(
                self._screen,
                self._LINE_COLOR,
                (0 + self._X_MARGIN, self._coordinates[i] + self._Y_MARGIN),
                (
                    self._coordinates[-1] + self._X_MARGIN,
                    self._coordinates[i] + self._Y_MARGIN,
                ),
            )

    def _draw_player_grid(self, player_id: int):
        """Draws the container grid that shows a player's available pieces."""
        x_margin = self._player_grid_margins[player_id][0]
        y_margin = self._player_grid_margins[player_id][1]

        # Draw the grid
        for i in range(6):  # Draw columns
            dest_y = y_margin + (
                self._piece_coordinates_y[-1]
                if i in (0, 1, 5)
                else self._piece_coordinates_y[-2]
            )
            pygame.draw.line(
                self._screen,
                self._LINE_COLOR,
                (self._piece_coordinates_x[i] + x_margin, 0 + y_margin),
                (
                    self._piece_coordinates_x[i] + x_margin,
                    dest_y,
                ),
            )
        for i in range(6):  # Draw rows
            pygame.draw.line(
                self._screen,
                self._LINE_COLOR,
                (0 + x_margin, self._piece_coordinates_y[i] + y_margin),
                (
                    self._piece_coordinates_x[-1] + x_margin,
                    self._piece_coordinates_y[i] + y_margin,
                ),
            )

    def _draw_player_grid_pieces(self, player_id: int, players: list[Player]):
        """Draws the available pieces of each player onto grids."""
        player = players[player_id]
        x_margin = self._player_grid_margins[player_id][0]
        y_margin = self._player_grid_margins[player_id][1]

        piece_id = 1
        # Go through coordinates of the grid
        for y in self._piece_coordinates_y[:-1]:
            for x in self._piece_coordinates_x[:-1]:
                # If piece is available show it
                if piece_id in player.available_pieces:
                    piece = player.pieces_copy[piece_id]

                    # Calculate the amount of padding needing so the piece is centered in the grid square
                    x_padding = (
                        self._PLAYER_GRID_WIDTH
                        - self._PLAYER_GRID_BOX_SIZE * len(piece[0])
                    ) / 2
                    y_padding = (
                        self._PLAYER_GRID_HEIGHT
                        - self._PLAYER_GRID_BOX_SIZE * len(piece)
                    ) / 2

                    # Display each square of each piece
                    for row in range(len(piece)):
                        for col in range(len(piece[0])):
                            if piece[row][col] == 0:
                                pygame.draw.rect(
                                    self._screen,
                                    self._player_colors[player_id],
                                    (
                                        (self._PLAYER_GRID_BOX_SIZE * col)
                                        + (x + x_margin + 1)
                                        + x_padding,
                                        (self._PLAYER_GRID_BOX_SIZE * row)
                                        + (y + y_margin + 1)
                                        + y_padding,
                                        self._PLAYER_GRID_BOX_SIZE,
                                        self._PLAYER_GRID_BOX_SIZE,
                                    ),
                                )
                else:
                    pygame.draw.rect(
                        self._screen,
                        self._BG_COLOR,
                        (
                            x + x_margin + 1,
                            y + y_margin + 1,
                            self._PLAYER_GRID_WIDTH,
                            self._PLAYER_GRID_HEIGHT,
                        ),
                    )
                    pass
                piece_id += 1

    def _update_score_text(self, player_id: int, players: list[Player]):
        """Updates the score of each player in each box."""
        player = players[player_id]
        text_surface = self.font.render(
            f"Squares left: {player.squares_left}", False, (0, 0, 0)
        )

        # Calculate the upper-left coordinate of the bounding box of the text
        x_margin = self._player_grid_margins[player_id][0]
        y_margin = self._player_grid_margins[player_id][1]
        x = self._piece_coordinates_x[-5] + x_margin + 1
        y = self._piece_coordinates_y[-2] + y_margin + 1

        # Clear the previous drawing
        pygame.draw.rect(
            self._screen,
            self._BG_COLOR,
            (
                x,
                y,
                self._PLAYER_GRID_WIDTH * 4,
                self._PLAYER_GRID_HEIGHT,
            ),
        )

        # Update x and y to center the text
        x += 65
        y += (self._PLAYER_GRID_HEIGHT - self._FONT_SIZE) / 2

        # Draw the text
        self._screen.blit(text_surface, (x, y))
