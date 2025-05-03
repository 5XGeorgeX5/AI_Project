class GomokuBoard:

    def __init__(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.n_moves = 0

    def is_winner(self) -> bool:
        # Check rows
        for i in range(15):
            for j in range(11):
                if (
                    self.board[i][j] != 0
                    and self.board[i][j]
                    == self.board[i][j + 1]
                    == self.board[i][j + 2]
                    == self.board[i][j + 3]
                    == self.board[i][j + 4]
                ):
                    return True
        # Check columns
        for i in range(11):
            for j in range(15):
                if (
                    self.board[i][j] != 0
                    and self.board[i][j]
                    == self.board[i + 1][j]
                    == self.board[i + 2][j]
                    == self.board[i + 3][j]
                    == self.board[i + 4][j]
                ):
                    return True
        # Check diagonals
        for i in range(11):
            for j in range(11):
                if (
                    self.board[i][j] != 0
                    and self.board[i][j]
                    == self.board[i + 1][j + 1]
                    == self.board[i + 2][j + 2]
                    == self.board[i + 3][j + 3]
                    == self.board[i + 4][j + 4]
                ):
                    return True
        # Check diagonals (reverse)
        for i in range(11):
            for j in range(4, 15):
                if (
                    self.board[i][j] != 0
                    and self.board[i][j]
                    == self.board[i + 1][j - 1]
                    == self.board[i + 2][j - 2]
                    == self.board[i + 3][j - 3]
                    == self.board[i + 4][j - 4]
                ):
                    return True
        return False

    def is_draw(self) -> bool:
        return not self.is_winner() and self.n_moves == 225  # 15x15 board

    def game_is_over(self) -> bool:
        return self.is_winner() or self.is_draw()

    def moves(self) -> int:
        return self.n_moves

    def update_board(self, i: int, j: int) -> bool:
        if 0 <= i < 15 and 0 <= j < 15 and self.board[i][j] == 0:
            self.board[i][j] = "X" if self.n_moves % 2 == 0 else "O"
            self.n_moves += 1
            return True
        return False

    def reset(self, i: int, j: int) -> None:
        if 0 <= i < 15 and 0 <= j < 15 and self.board[i][j] != 0:
            self.board[i][j] = 0
            self.n_moves -= 1
        else:
            raise ValueError("Invalid position to reset.")

    def display_board(self) -> None:
        for row in self.board:
            print(" ".join("-" if cell == 0 else cell for cell in row))

    def reset_board(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.n_moves = 0
