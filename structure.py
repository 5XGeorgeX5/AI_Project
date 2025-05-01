class GomokuBoard:

    def __init__(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.n_moves = 0

    def is_winner(self) -> bool:
        # to be implemented
        pass

    def is_draw(self) -> bool:
        # to be implemented
        pass

    def game_is_over(self) -> bool:
        # to be implemented
        pass

    def moves(self) -> int:
        return self.n_moves

    def update_board(self, i: int, j: int) -> bool:
        # to be implemented
        pass

    def reset(self, i: int, j: int) -> None:
        # to be implemented
        pass

    def display_board(self) -> None:
        # to be implemented
        pass

    def reset_board(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.n_moves = 0

    def heuristic(self) -> int:
        # to be implemented -> George
        pass

    def get_state(self) -> str:
        # to be implemented -> George
        pass


# Players
# ___________________________________


class Player:

    def get_move(self) -> tuple[int, int]:
        raise NotImplementedError


class GomokuPlayer(Player):

    def get_move(self) -> tuple[int, int]:
        # to be implemented
        pass


class BaseAIPlayer(Player):
    def __init__(self, board: GomokuBoard):
        self.board = board

    def get_move(self) -> int:
        raise NotImplementedError


class MiniMaxAIPlayer(BaseAIPlayer):
    def __init__(self, board: GomokuBoard):
        super().__init__(board)

    def minimax(self, depth: int) -> int:
        # to be implemented
        pass

    def get_move(self) -> tuple[int, int]:
        # to be implemented
        pass


class AlphaNetaAIPlayer(BaseAIPlayer):
    def __init__(self, board: GomokuBoard):
        super().__init__(board)

    def minimax(self, alpha: int, beta: int, depth: int) -> int:
        # to be implemented
        pass

    def get_move(self) -> tuple[int, int]:
        # to be implemented
        pass


class GUI:

    def __init__(self, board: GomokuBoard):
        self.board = board

    # no idea what methods to implement here


class GameManager:

    def __init__(self, board: GomokuBoard, players: tuple[Player, Player]):
        self.board = board
        self.players = players

    def run(self):
        # to be implemented: run game loop
        pass
