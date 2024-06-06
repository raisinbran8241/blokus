import pygame
from game_board import GameBoard
from graphics_handler import GraphicsHandler
from player import Player
from piece import Piece


class Game:
    """Merges all the parts of the game together."""

    def __init__(self, num_players: int):
        self._game_state = 0  # 0: start, 1: in game, 2: rules menu, 3: game over
        self._num_players = num_players
        self._board = GameBoard(20, 20)
        self._current_player = -1
        self._graphics_handler = GraphicsHandler()
        self._players: list[Player] = []
        self._has_legal_moves = [True] * self._num_players
        for i in range(num_players):
            self._players.append(Player("", i))

    def start_game(self):
        self._game_state = 1

    @property
    def num_players(self):
        return self._num_players

    @property
    def board(self):
        return self._board

    @property
    def current_player(self):
        return self._current_player

    @property
    def players(self):
        return self._players

    def _update_turn(self) -> None:
        """Updates current_player to the ID of the next player"""
        if self._current_player + 1 == self._num_players:
            self._board.toggle_first_move()
        self._current_player = (self._current_player + 1) % self._num_players

        if not self._has_legal_moves[self._current_player]:
            self._update_turn()
        else:
            if not self.can_play_move():
                self._has_legal_moves[self.current_player] = False

                if self._has_legal_moves == [False] * 4:
                    self._game_state = 3

                self._update_turn()

    def _find_winner(self) -> list[int]:
        """Finds the player(s) with the highest score."""
        winners = []
        max_score = -100

        for i in range(4):
            squares_left = self.players[i].squares_left
            if squares_left > max_score:
                winners = [i]
            elif squares_left == max_score:
                winners.append(i)

        return winners

    def can_play_move(self) -> bool:
        """Checks if the current player has any legal moves."""
        player = self._players[self.current_player]
        available_pieces = player.available_pieces
        for piece_id in available_pieces:
            piece = player.pieces_copy[piece_id]

            # Check all rotations before the piece is flipped horizontally
            if self._check_all_rotations(piece):
                return True

            # Check all rotations when piece is flipped horizontally
            piece.flip_horizontally()
            if self._check_all_rotations(piece):
                return True
            piece.flip_horizontally()

            # Check all rotations when piece is flipped vertically
            piece.flip_vertically()
            if self._check_all_rotations(piece):
                return True
            piece.flip_vertically()

        return False

    def _check_all_rotations(self, piece: Piece) -> bool:
        for i in range(4):
            piece.rotate_clockwise()
            if self._board.can_place_piece(piece, self.current_player):
                return True
        return False

    def handle_mouse(self, event: pygame.event.Event, coords: tuple) -> None:
        if self._game_state == 0:
            # Updates the main menu based on where the mouse is hovering
            if 520 <= coords[0] <= 880 and 390 <= coords[1] <= 510:
                self._graphics_handler.update_main_menu(True, False)
            elif 520 <= coords[0] <= 880 and 540 <= coords[1] <= 660:
                self._graphics_handler.update_main_menu(False, True)
            else:
                self._graphics_handler.update_main_menu(False, False)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 520 <= coords[0] <= 880 and 390 <= coords[1] <= 510:
                    self._game_state = 2
                    self._update_turn()
                elif 520 <= coords[0] <= 880 and 540 <= coords[1] <= 660:
                    self._game_state = 1

        elif self._game_state == 2:  # In game
            # Get the coordinates and check if it is an actual move
            square = self._graphics_handler.get_square_from_coords(coords)
            if -1 in square:
                return

            # No pieces left or no legal moves? Skip the turn
            player = self._players[self._current_player]
            piece = player.get_piece()

            # Places a piece on left click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._board.place_piece(
                    piece, square[0], square[1], self._current_player
                ):
                    player.use_piece()
                    self._update_turn()

            # Update the shadow board and screen
            self._board.update_shadow(piece, square[0], square[1], self._current_player)
            self._graphics_handler.update_game_screen(
                self._board, self.current_player, self.players
            )

        elif self._game_state == 3:  # Finished game
            scores = []
            max_score = -100
            for i in range(4):
                player = self.players[i]

                # Score calculation
                score = -player.squares_left
                if len(player.available_pieces) == 0:
                    score += 15
                    if player.last_piece_played == 1:
                        score += 5

                # Winner calculation
                scores.append(score)
                if score > max_score:
                    max_score = score
                    winners = [i]
                elif score == max_score:
                    winners.append(i)

            if 520 <= coords[0] <= 880 and 540 <= coords[1] <= 660:
                self._graphics_handler.update_game_over_screen(True, scores, winners)
            else:
                self._graphics_handler.update_game_over_screen(False, scores, winners)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 520 <= coords[0] <= 880 and 540 <= coords[1] <= 660:
                    self._game_state = 0
                    self._update_turn()

    def handle_keyboard(self, event: pygame.event.Event) -> None:
        player = self._players[self._current_player]
        piece = player.get_piece()
        if event.key == pygame.K_x:
            piece.rotate_clockwise()
        elif event.key == pygame.K_z:
            piece.rotate_counterclockwise()
        elif event.key == pygame.K_a:
            piece.flip_vertically()
        elif event.key == pygame.K_s:
            piece.flip_horizontally()
        elif event.key == pygame.K_LEFT:
            player.left_piece()
        elif event.key == pygame.K_RIGHT:
            player.right_piece()
        elif event.key == pygame.K_DOWN:
            player.down_piece()
        elif event.key == pygame.K_UP:
            player.up_piece()

        if self._game_state == 1:
            self._graphics_handler.update_game_screen(
                self._board, self.current_player, self.players
            )
