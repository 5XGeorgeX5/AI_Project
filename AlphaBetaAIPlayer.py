from structure import BaseAIPlayer
from GomokuBoard import GomokuBoard


class AlphaBetaAIPlayer(BaseAIPlayer):
    __depth = 2
    __isBlack = None

    def __init__(self, board: GomokuBoard):
        super().__init__(board)

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

        start = corners[0] * 15 + corners[1]
        end = corners[2] * 15 + corners[3]
        length = corners[3] - corners[1] + 1

        if maximizingPlayer:
            maxEval = -500000000
            while start < end:
                for j in range(start, start + length):
                    if self.board.update_board(j):
                        value = self.minimax(False, depth - 1, alpha, beta)
                        maxEval = max(maxEval, value)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                        alpha = max(alpha, value)
                        if beta <= alpha:
                            return maxEval
                start += 15
            return maxEval
        else:
            minEval = 500000000
            while start < end:
                for j in range(start, start + length):
                    if self.board.update_board(j):
                        value = self.minimax(True, depth - 1, alpha, beta)
                        minEval = min(minEval, value)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                        beta = min(beta, value)
                        if beta <= alpha:
                            return minEval
                start += 15
            return minEval

    def get_move(self) -> int:
        self.__isBlack = (self.board.moves() % 2) == 0
        if self.board.moves() == 0:
            return 112  # position 8, 8
        index = -1
        alpha = -500000000
        beta = 500000000

        corners = self.board.get_corners()

        start = corners[0] * 15 + corners[1]
        end = corners[2] * 15 + corners[3]
        length = corners[3] - corners[1] + 1

        result = 0
        if self.__isBlack:
            maxEval = -500000000
            while start < end:
                for j in range(start, start + length):
                    if self.board.update_board(j):
                        value = self.minimax(False, self.__depth - 1, alpha, beta)
                        if value > maxEval:
                            index = j
                            maxEval = value
                            result = value
                        alpha = max(alpha, value)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                start += 15
        else:
            minEval = 500000000
            while start < end:
                for j in range(start, start + length):
                    if self.board.update_board(j):
                        value = self.minimax(True, self.__depth - 1, alpha, beta)
                        if value < minEval:
                            index = j
                            minEval = value
                            result = value
                        beta = min(beta, value)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                start += 15
        print(
            f"{(index // 15 + 1, index % 15 + 1)}: {result}, moves: {self.board.moves() + 1}"
        )
        return index
