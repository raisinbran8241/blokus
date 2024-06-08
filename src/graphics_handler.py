import pygame
from game_board import GameBoard
from player import Player


class GraphicsHandler:
    """Handles the graphical aspects of the game, such as drawing and updating the board and pieces."""

    def __init__(self):
        # Set up the graphical environment
        self._screen = pygame.display.set_mode((1400, 750))
        self._BG_COLOR = (160, 160, 160)
        self._HIGHLIGHT_COLOR = (253, 255, 50)
        self._X_MARGIN = 440
        self._Y_MARGIN = 160
        self._GRID_BOX_SIZE = 25
        self._PLAYER_GRID_HEIGHT = 65
        self._PLAYER_GRID_WIDTH = 80
        self._PLAYER_GRID_BOX_SIZE = 15

        self._screen.fill(self._BG_COLOR)
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

        # Draw player grids (5x4, 4 players)
        self._piece_coordinates_x = []
        self._piece_coordinates_y = []
        for i in range(6):
            self._piece_coordinates_x.append(i * self._PLAYER_GRID_WIDTH + i)
        for i in range(6):
            self._piece_coordinates_y.append(i * self._PLAYER_GRID_HEIGHT + i)

        self._player_grid_margins = [(984, 30), (984, 394), (15, 394), (15, 30)]

    def update_main_menu(self, play_button: bool, rules_button: bool) -> None:
        # Fill in screen to redraw everything
        self._screen.fill(self._BG_COLOR)

        bold_font = pygame.font.Font("./FiraCode-SemiBold.ttf", 84)
        text_surface = bold_font.render("Blokus", False, (0, 0, 0))
        self._screen.blit(text_surface, (550, 200))

        font = pygame.font.SysFont("Fira Code", 50)
        # Expand buttons when hovered over
        if play_button:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (520, 395, 374, 110),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 44)
            self._screen.blit(font.render("Start", False, (0, 0, 0)), (635, 426))
        else:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (530, 400, 340, 100),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 40)
            self._screen.blit(font.render("Start", False, (0, 0, 0)), (640, 430))
        if rules_button:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (520, 545, 374, 110),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 44)
            self._screen.blit(font.render("Rules", False, (0, 0, 0)), (635, 576))
        else:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (530, 550, 340, 100),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 40)
            self._screen.blit(font.render("Rules", False, (0, 0, 0)), (640, 580))

    def blur_screen(self):
        alpha_surface = pygame.Surface((1400, 750), pygame.SRCALPHA)
        alpha_value = 128
        alpha_surface.fill(self._BG_COLOR + (alpha_value,))

        self._screen.blit(alpha_surface, (0, 0))

    def update_about_screen(self, back_button):
        # Blur the rest of the screen
        rect = pygame.Rect(400, 75, 600, 625)
        pygame.draw.rect(self._screen, self._BG_COLOR, rect, border_radius=20)
        pygame.draw.rect(self._screen, (0, 0, 0), rect, width=5, border_radius=20)

        font = pygame.font.SysFont("Fira Code", 14)
        text = """
        The first piece played by each player must cover a corner\n 
        square. Each new piece must touch at least one other piece\n 
        of the same color, but only at the corners. Pieces of the\n 
        same color can never touch along a side.\n\n 
        Whenever a player is unable to place a piece on the board,\n 
        that player must pass their turn. The game ends when neither\n 
        player can place any more pieces.\n\n
        The scores for each player depend on how many squares\n 
        there are in their remaining pieces. 1 square = -1 point.\n 
        A player earns +15 points if all of their pieces have been\n 
        placed on the board plus 5 bonus points if the last piece\n 
        they placed on the board was the smallest piece.\n
        """

        for i, line in enumerate(text.splitlines()):
            self._screen.blit(font.render(line, False, (0, 0, 0)), (360, 140 + 12 * i))

        if back_button:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (520, 500, 374, 110),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 44)
            self._screen.blit(font.render("Back", False, (0, 0, 0)), (640, 531))
        else:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (530, 505, 340, 100),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 40)
            self._screen.blit(font.render("Back", False, (0, 0, 0)), (645, 535))

    def update_game_screen(
        self, game_board: GameBoard, current_player: int, players: list[Player]
    ) -> None:
        """Updates the squares based on the state of the board."""

        # Turn indicator
        font = pygame.font.SysFont("Fira Code", 30)
        text_surface = font.render("'s turn", False, (0, 0, 0))
        self._screen.blit(text_surface, (700, 70))
        pygame.draw.rect(
            self._screen, self._player_colors[current_player], (670, 70, 30, 30)
        )

        self._draw_game_grid()

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
            self._draw_player_grid(i)

        self._highlight_piece(current_player, players)

    def update_game_over_screen(
        self, home_button: bool, scores: list[int], winners: list[int]
    ):
        # Fill in screen to redraw everything
        self._screen.fill(self._BG_COLOR)

        font = pygame.font.SysFont("Fira Code", 50)
        text_surface = font.render("Winners: ", False, (0, 0, 0))
        self._screen.blit(text_surface, (565 - 35 * len(winners), 150))

        for i in range(len(winners)):
            pygame.draw.rect(
                self._screen,
                self._player_colors[winners[i]],
                (775 + (50 + 25) * (i + 1) - 30 * len(winners), 150, 50, 50),
            )  # This just works trust

        font = pygame.font.SysFont("Fira Code", 25)
        for i in range(len(scores)):
            pygame.draw.rect(
                self._screen,
                self._player_colors[i],
                (200 + 312.5 * i, 330, 50, 50),
            )
            text_surface = font.render(f"Score: {scores[i]}", False, (0, 0, 0))
            self._screen.blit(text_surface, (200 + 312.5 * i - 50, 440))

        # Expand button if hovered over
        if home_button:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (520, 545, 374, 110),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 44)
            self._screen.blit(font.render("Home", False, (0, 0, 0)), (645, 576))
        else:
            pygame.draw.rect(
                self._screen,
                (0, 0, 0),
                (530, 550, 340, 100),
                width=3,
                border_radius=20,
            )
            font = pygame.font.SysFont("Fira Code", 40)
            self._screen.blit(font.render("Home", False, (0, 0, 0)), (650, 580))

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

        # If the square is out of bounds, return boundary index so that things can still be updated
        if y < self._Y_MARGIN:
            square[0] = 0
        elif y > self._Y_MARGIN + self._coordinates[-1]:
            square[0] = 19
        if x < self._X_MARGIN:
            square[1] = 0
        elif x > self._X_MARGIN + self._coordinates[-1]:
            square[1] = 19

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
                # Clear the space first (from highlights)
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
                piece_id += 1

    def _highlight_piece(self, player_id: int, players: list[Player]):
        player = players[player_id]
        piece_id = player.piece_id
        x = self._player_grid_margins[player_id][0] + (self._PLAYER_GRID_WIDTH + 1) * (
            (piece_id - 1) % 5
        )
        y = self._player_grid_margins[player_id][1] + (self._PLAYER_GRID_HEIGHT + 1) * (
            (piece_id - 1) // 5
        )
        pygame.draw.rect(
            self._screen,
            self._HIGHLIGHT_COLOR,
            (
                x,
                y,
                self._PLAYER_GRID_WIDTH + 2,
                self._PLAYER_GRID_HEIGHT + 2,
            ),
            width=3,
        )

    def _update_score_text(self, player_id: int, players: list[Player]):
        """Updates the score of each player in each box."""
        player = players[player_id]
        font = pygame.font.SysFont("Fira Code", 20)
        text_surface = font.render(f"Score: {-player.squares_left}", False, (0, 0, 0))

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
        x += 100
        y += (self._PLAYER_GRID_HEIGHT - 20) / 2

        # Draw the text
        self._screen.blit(text_surface, (x, y))
