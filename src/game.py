import pygame
from game_board import GameBoard
from graphics_handler import GraphicsHandler
from player import Player


class Game:
    """Merges all the parts of the game together."""

    def __init__(self, num_players: int):
        self._num_players = num_players
        self._board = GameBoard(20, 20)
        self._current_player = 0
        self._graphics_handler = GraphicsHandler()
        self._players: list[Player] = []
        for i in range(num_players):
            self._players.append(Player("", i))

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

    def update_turn(self):
        """Updates self._current_player. 0 to 1, 1 to 2, etc."""
        if self._current_player + 1 == self._num_players:
            self._board.toggle_first_move()
        self._current_player = (self._current_player + 1) % self._num_players

    def handle_mouse(self, event: pygame.event.Event, coords: tuple):
        # Get the coordinates and check if it is an actual move
        square = self._graphics_handler.get_square_from_coords(coords)
        if -1 in square:
            return

        # No pieces left? Skip the turn
        player = self._players[self._current_player]
        if player.all_pieces_used:  # Will update later
            self.update_turn()

        player.set_to_lowest_value_piece()
        piece = player.get_piece()

        # Places a piece on left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._board.place_piece(
                piece, square[0], square[1], self._current_player
            ):
                player.use_piece()
                self.update_turn()

        # Update the shadow board
        self._board.update_shadow(piece, square[0], square[1], self._current_player)

        # Update the screen
        self._graphics_handler.update_screen(
            self._board, self.current_player, self.players
        )

    def handle_keyboard(self, event: pygame.event.Event):
        # TODO: Add reflecting pieces
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
