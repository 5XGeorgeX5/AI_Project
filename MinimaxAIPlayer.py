from structure import BaseAIPlayer
from GomokuBoard import GomokuBoard


class MiniMaxAIPlayer(BaseAIPlayer):
    __depth = 3

    def __init__(self, board: GomokuBoard):
        super().__init__(board)

    def minimax(self, maximizingPlayer: bool, depth: int) -> int:
        if self.board.is_win():
            if maximizingPlayer:
                return -500000 + self.board.moves()
            else:
                return 500000 - self.board.moves()
        elif self.board.moves() == 225:
            return 0
        elif depth == 0:
            return self.board.heuristic()

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
        if maximizingPlayer:
            maxEval = -500000000
            while i < end:
                for j in range(i, i + length):
                    if self.board.update_board(j):
                        eval = self.minimax(False, depth - 1)
                        maxEval = max(maxEval, eval)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                i += 15
            return maxEval
        else:
            minEval = 500000000
            while i < end:
                for j in range(i, i + length):
                    if self.board.update_board(j):
                        eval = self.minimax(True, depth - 1)
                        minEval = min(minEval, eval)
                        self.board.reset(j)
                        self.board.set_corners(corners)
                i += 15
            return minEval

    def get_move(self) -> int:
        maximizingPlayer = (self.board.moves() % 2) == 0
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
        if maximizingPlayer:
            maxEval = -500000000
            while i < end:
                for j in range(i, i + length):
                    if self.board.update_board(j):
                        value = self.minimax(False, self.__depth - 1)
                        if value > maxEval:
                            index = j
                            maxEval = value

                        self.board.reset(j)
                        self.board.set_corners(corners)
                i += 15
        else:
            minEval = 500000000
            while i < end:
                for j in range(i, i + length):
                    if self.board.update_board(j):
                        value = self.minimax(True, self.__depth - 1)
                        if value < minEval:
                            index = j
                            minEval = value

                        self.board.reset(j)
                        self.board.set_corners(corners)
                i += 15
            print(minEval)
        if index == -1:
            raise ValueError("george is stupid")
        return index
