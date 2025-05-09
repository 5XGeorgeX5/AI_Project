from structure import BaseAIPlayer
from GomokuBoard import GomokuBoard


class AlphaBetaAIPlayer(BaseAIPlayer):
    __depth = 2

    def __init__(self, board: GomokuBoard):
        super().__init__(board)

    def minimax(self, depth: int, alpha: int, beta: int) -> int:
        self.runs += 1
        if self.board.is_win():
            return self.board.moves() - 500000
        elif self.board.moves() == 225:
            return 0
        elif depth == 0:
            return self.board.heuristic()

        corners = self.board.get_corners()
        row = corners[0]
        col = corners[1]
        if row == 0:
            row = 1
        if col == 0:
            col = 1

        start = (row - 1) * 15 + (col - 1)

        row = corners[2]
        col = corners[3]

        if row == 14:
            row = 13
        if col == 14:
            col = 13

        end = (row + 1) * 15 + (col + 1)
        length = corners[3] - corners[1] + 3
        i = start
        result = -500000000
        while i < end:
            for j in range(i, i + length):
                if self.board.update_board(j):
                    value = -self.minimax(depth - 1, -beta, -alpha)
                    self.board.reset(j)
                    self.board.set_corners(corners)
                    result = max(result, value)
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        return alpha
            i += 15
        return result

    def get_move(self) -> int:
        if self.board.moves() == 0:
            return (7 - 1) * 15 + (7 - 1)
        index = -1

        corners = self.board.get_corners()
        row = corners[0]
        colm = corners[1]
        if row == 0:
            row = 1
        if colm == 0:
            colm = 1

        start = (row - 1) * 15 + (colm - 1)

        row = corners[2]
        colm = corners[3]

        if row == 14:
            row = 13
        if colm == 14:
            colm = 13

        end = (row + 1) * 15 + (colm + 1)
        length = corners[3] - corners[1] + 3
        i = start
        opponentScore = 500000000
        while i < end:
            for j in range(i, i + length):
                if self.board.update_board(j):
                    value = self.minimax(self.__depth - 1, -500000000, opponentScore)
                    self.board.reset(j)
                    self.board.set_corners(corners)
                    if value < opponentScore:
                        index = j
                        opponentScore = value
            i += 15
        if index == -1:
            raise ValueError("george is stupid")
        return index
