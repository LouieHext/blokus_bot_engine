import logging
from blokus.board import Board
from blokus.board_states import BoardStatesEnum
from blokus.player.base_player import BasePlayer
from blokus.exceptions import InvalidMove

class Game:
    def __init__(self, board: Board, players: list[BasePlayer], timeout: float = 30):
        self._board = board
        self._players = players
        self._validate_game()
        self._timeout = timeout
        self.__unable_to_play = []

    @property
    def board(self) -> Board:
        """Returns the board associated with the game

        Returns:
            Board: board
        """
        return self._board

    @property
    def players(self) -> list[BasePlayer]:
        """Returns the players associated with the game

        Returns:
            list[BasePlayer]: players
        """
        return self._players

    @property
    def timeout(self) -> float:
        """Returns the timeout associated with the game

        Returns:
            float: timeout
        """
        return self.timeout

    @property
    def unable_to_play(self) -> list[BoardStatesEnum]:
        """Returns the players that are unable to play

        Returns:
            list[BoardStatesEnum]: players with no moves
        """
        return self.__unable_to_play

    @property
    def player_colours(self) -> list[BoardStatesEnum]:
        """Returns a list of player colours

        Returns:
            list[BoardStatesEnum]: player colours
        """
        return BoardStatesEnum.get_player_colours()

    def play_game(self, display: bool = True)-> list[BasePlayer]:
        """Plays the game,
        this continues until all players are unable to move.
        Returns the rankings of the players

        Args:
            display (bool, optional): If to display the game. Defaults to True.

        Returns:
            list[BasePlayer]: players ranked by score
        """
        while len(self.unable_to_play) != len(self.player_colours):
            self.play_turn()
            if display:
                self.board.display_board()
            logging.info(self.board.get_score_str())
        self.board.print_times()
        if display:
            self.board.display_board(stop_code=True)
        print(f"FINAL SCORE: {self.board.get_score_str()}")
        return sorted(self.players, key = lambda x: self.board.get_score_for_colour(x.colour))
        
    def play_turn(self):
        """Plays a single turn for all players

        Args:
            time_out (float, optional): Max time to find move. Defaults to 30.
        """
        for colour in self.player_colours:
            self.play_turn_for_colour(colour)

    def play_turn_for_colour(self, colour: BoardStatesEnum):
        """Plays a move for the supplied colour.
        skips the colour if it was previously unable to play a move

        Args:
            colour (BoardStatesEnum): colour to play
        """
        if colour in self.unable_to_play:
            return
        # finidng valid moves for player
        valid_moves = self.board.get_valid_moves_for_colour(colour)
        if not valid_moves:
            logging.info(f"{colour} is unable to play")
            self.__unable_to_play.append(colour)
            return
        # get the player to select the best move
        player = self.get_player_by_colour(colour)
        chosen_move = player.select_best_move(valid_moves)
        if not chosen_move:
            return
        # play the move
        try:
            self.board.play_move(chosen_move)
        except InvalidMove:
            logging.info(f"Player {colour} made an invalid move")

    def _validate_game(self):
        """Validates that the game is valid,
        this checks that 4 players are present and they
        each have a different colour

        Raises:
            ValueError: if not 4 players are present
            ValueError: if not all the colours are present
        """
        # check player count
        if len(self.players) != 4:
            raise ValueError(f"Game requires 4 players not {len(self.players)}")
        # check the colours
        active_colours = [p.colour for p in self.players]
        for colour in self.player_colours:
            if colour in active_colours:
                continue
            raise ValueError(f"Not all colours are present, {active_colours}")

    def get_player_by_colour(self, colour: BoardStatesEnum) -> BasePlayer:
        """Gets the player associated with a specific colour

        Args:
            colour (BoardStatesEnum): colour to find player for

        Returns:
            BasePlayer: player
        """
        player = [p for p in self.players if p.colour == colour][0]
        return player
