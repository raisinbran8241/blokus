from game_board import GameBoard
from graphics_handler import GraphicsHandler
from player import Player


class Game:
    """Merges all the parts of the game together."""

    def __init__(self, num_players):
        self._num_players = num_players
        self._board = GameBoard(20, 20)
        self._current_player = 0
        self._graphics_handler = GraphicsHandler()
        self._players: list[Player] = []
        for i in range(num_players):
            self._players.append(Player("", i))

        self._players[0].selected_piece_id = 12
        player = self._players[self.current_player]
        piece = player.get_piece_from_id(player.selected_piece_id)
        print(piece)
        self._board.place_piece(piece, 0, 17, self._current_player)
        self._graphics_handler.update_screen(self._board)

    @property
    def num_players(self):
        return self._num_players

    @property
    def board(self):
        return self._board

    @property
    def current_player(self):
        return self._current_player

    def update_turn(self):
        """Updates self._current_player. For example, it goes from 0 to 1, 1 to 2, etc."""
        self._current_player = (self._current_player + 1) % self._num_players
