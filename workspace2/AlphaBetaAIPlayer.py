from structure import BaseAIPlayer
from GomokuBoard import GomokuBoard


class AlphaBetaAIPlayer(BaseAIPlayer):
    __depth = 2
    __isBlack = None

    def __init__(self, board: GomokuBoard, depth: int = 2):
        super().__init__(board)
        self.__depth = depth

    def minimax(self, maximizingPlayer: bool, depth: int, alpha: int, beta: int) -> int:
        self.runs += 1
        if self.board.is_win():
            if maximizingPlayer:
                return -500000 + self.board.moves()
            else:
                return 500000 - self.board.moves()
        elif self.board.moves() == 225:
            return 0
        elif depth == 0:
            blackScore, whiteScore = self.board.heuristic()
            if self.__isBlack:
                return blackScore - whiteScore * 3
            else:
                return blackScore * 3 - whiteScore

        corners = self.board.get_corners()

        moves = self.valideMoves()

        if maximizingPlayer:
            maxEval = -500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(False, depth - 1, alpha, beta)
                self.board.reset(move)
                self.board.set_corners(corners)
                maxEval = max(maxEval, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    return maxEval
            return maxEval
        else:
            minEval = 500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(True, depth - 1, alpha, beta)
                self.board.reset(move)
                self.board.set_corners(corners)
                minEval = min(minEval, value)
                beta = min(beta, value)
                if beta <= alpha:
                    return minEval
            return minEval

    def get_move(self) -> int:
        self.__isBlack = (self.board.moves() % 2) == 0
        if self.board.moves() == 0:
            return 112  # position 8, 8
        index = -1
        alpha = -500000000
        beta = 500000000

        corners = self.board.get_corners()

        moves = self.valideMoves()

        result = 0
        if self.__isBlack:
            maxEval = -500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(False, self.__depth - 1, alpha, beta)
                self.board.reset(move)
                self.board.set_corners(corners)
                if value > maxEval:
                    index = move
                    maxEval = value
                    result = value
                    alpha = value
        else:
            minEval = 500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(True, self.__depth - 1, alpha, beta)
                self.board.reset(move)
                self.board.set_corners(corners)
                if value < minEval:
                    index = move
                    minEval = value
                    result = value
                    beta = value
        print(
            f"{(index // 15 + 1, index % 15 + 1)}: {result}, moves: {self.board.moves() + 1}"
        )
        return index
