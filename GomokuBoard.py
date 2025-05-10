class TileType:
    EMPTY = 0
    BLACK = 7
    WHITE = 11


class GomokuBoard:
    __lastMove = None
    # region winning_positions
    __winning_positions = None
    # endregion

    BOARD_SIZE = 15
    # -- Pattern dictionary using "X" as placeholder --

    # region lines
    __lines = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
        [45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74],
        [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89],
        [90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104],
        [105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119],
        [120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134],
        [135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149],
        [150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164],
        [165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179],
        [180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194],
        [195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209],
        [210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224],
        [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210],
        [1, 16, 31, 46, 61, 76, 91, 106, 121, 136, 151, 166, 181, 196, 211],
        [2, 17, 32, 47, 62, 77, 92, 107, 122, 137, 152, 167, 182, 197, 212],
        [3, 18, 33, 48, 63, 78, 93, 108, 123, 138, 153, 168, 183, 198, 213],
        [4, 19, 34, 49, 64, 79, 94, 109, 124, 139, 154, 169, 184, 199, 214],
        [5, 20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215],
        [6, 21, 36, 51, 66, 81, 96, 111, 126, 141, 156, 171, 186, 201, 216],
        [7, 22, 37, 52, 67, 82, 97, 112, 127, 142, 157, 172, 187, 202, 217],
        [8, 23, 38, 53, 68, 83, 98, 113, 128, 143, 158, 173, 188, 203, 218],
        [9, 24, 39, 54, 69, 84, 99, 114, 129, 144, 159, 174, 189, 204, 219],
        [10, 25, 40, 55, 70, 85, 100, 115, 130, 145, 160, 175, 190, 205, 220],
        [11, 26, 41, 56, 71, 86, 101, 116, 131, 146, 161, 176, 191, 206, 221],
        [12, 27, 42, 57, 72, 87, 102, 117, 132, 147, 162, 177, 192, 207, 222],
        [13, 28, 43, 58, 73, 88, 103, 118, 133, 148, 163, 178, 193, 208, 223],
        [14, 29, 44, 59, 74, 89, 104, 119, 134, 149, 164, 179, 194, 209, 224],
        [10, 26, 42, 58, 74],
        [9, 25, 41, 57, 73, 89],
        [8, 24, 40, 56, 72, 88, 104],
        [7, 23, 39, 55, 71, 87, 103, 119],
        [6, 22, 38, 54, 70, 86, 102, 118, 134],
        [5, 21, 37, 53, 69, 85, 101, 117, 133, 149],
        [4, 20, 36, 52, 68, 84, 100, 116, 132, 148, 164],
        [3, 19, 35, 51, 67, 83, 99, 115, 131, 147, 163, 179],
        [2, 18, 34, 50, 66, 82, 98, 114, 130, 146, 162, 178, 194],
        [1, 17, 33, 49, 65, 81, 97, 113, 129, 145, 161, 177, 193, 209],
        [0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224],
        [15, 31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191, 207, 223],
        [30, 46, 62, 78, 94, 110, 126, 142, 158, 174, 190, 206, 222],
        [45, 61, 77, 93, 109, 125, 141, 157, 173, 189, 205, 221],
        [60, 76, 92, 108, 124, 140, 156, 172, 188, 204, 220],
        [75, 91, 107, 123, 139, 155, 171, 187, 203, 219],
        [90, 106, 122, 138, 154, 170, 186, 202, 218],
        [105, 121, 137, 153, 169, 185, 201, 217],
        [120, 136, 152, 168, 184, 200, 216],
        [135, 151, 167, 183, 199, 215],
        [150, 166, 182, 198, 214],
        [4, 18, 32, 46, 60],
        [5, 19, 33, 47, 61, 75],
        [6, 20, 34, 48, 62, 76, 90],
        [7, 21, 35, 49, 63, 77, 91, 105],
        [8, 22, 36, 50, 64, 78, 92, 106, 120],
        [9, 23, 37, 51, 65, 79, 93, 107, 121, 135],
        [10, 24, 38, 52, 66, 80, 94, 108, 122, 136, 150],
        [11, 25, 39, 53, 67, 81, 95, 109, 123, 137, 151, 165],
        [12, 26, 40, 54, 68, 82, 96, 110, 124, 138, 152, 166, 180],
        [13, 27, 41, 55, 69, 83, 97, 111, 125, 139, 153, 167, 181, 195],
        [14, 28, 42, 56, 70, 84, 98, 112, 126, 140, 154, 168, 182, 196, 210],
        [29, 43, 57, 71, 85, 99, 113, 127, 141, 155, 169, 183, 197, 211],
        [44, 58, 72, 86, 100, 114, 128, 142, 156, 170, 184, 198, 212],
        [59, 73, 87, 101, 115, 129, 143, 157, 171, 185, 199, 213],
        [74, 88, 102, 116, 130, 144, 158, 172, 186, 200, 214],
        [89, 103, 117, 131, 145, 159, 173, 187, 201, 215],
        [104, 118, 132, 146, 160, 174, 188, 202, 216],
        [119, 133, 147, 161, 175, 189, 203, 217],
        [134, 148, 162, 176, 190, 204, 218],
        [149, 163, 177, 191, 205, 219],
        [164, 178, 192, 206, 220],
    ]
    # endregion
    PATTERN_SCORES = {
        (0, 1, 1, 1, 1, 0): 10000,
        (1, 1, 1, 1, 0): 7000,
        (0, 1, 1, 1, 1): 7000,
        # "X_XXX": 1000,
        # "XX_XX": 1000,
        # "XXX_X": 1000,
        (0, 0, 1, 1, 1, 0, 0): 4000,
        (0, 1, 1, 1, 0): 3000,
        # "X__XX": 100,
        # "XX__X": 100,
        # "X_X_X": 100,
        (0, 0, 1, 1, 0, 0): 200,
        (0, 1, 1, 0): 100,
        (1, 0, 1): 10,
    }

    # -- Get all lines from board (rows, cols, diagonals) --
    def get_lines(self) -> list[list[int]]:
        return [[self.board[i] for i in line] for line in self.__lines]

    # -- Convert int line to string line (for given symbol) --
    def getKey(self, line: list[int], symbol: int) -> tuple[int, ...]:
        return tuple(
            (1 if i == symbol else -1 if i != TileType.EMPTY else 0) for i in line
        )

    # -- Count how many times each pattern appears --
    def count_patterns(self, key: tuple) -> int:
        score = 0
        for pattern, val in self.PATTERN_SCORES.items():
            i = 0
            size = len(key) - len(pattern)
            len_pattern = len(pattern)
            while i <= size:
                if key[i : i + len_pattern] == pattern:
                    score += val
                    i += 1
                else:
                    i += 1
        return score

    # -- Final evaluation --
    def evaluate_board(self, symbol: int) -> int:
        total_score = 0
        for line in self.get_lines():
            key = self.getKey(line, symbol)
            total_score += self.count_patterns(key)
        return total_score

    # -- For Minimax scoring --
    def evaluate_board_for_minimax(self) -> int:
        return self.evaluate_board(TileType.BLACK) - self.evaluate_board(TileType.WHITE)

    def __init__(self):
        self.board = [TileType.EMPTY] * 225
        self.n_moves = 0
        self.corners = [
            50000,
            50000,
            -50000,
            -50000,
        ]  # [start row, start colm, end row , end colm]
        self.__winning_positions = self.get_winnig_positions()

    def get_winnig_positions(self) -> list[list[int]]:
        # Check rows
        myList = []
        for i in range(15):
            for j in range(11):
                myList.append(
                    [
                        i * 15 + j,
                        i * 15 + j + 1,
                        i * 15 + j + 2,
                        i * 15 + j + 3,
                        i * 15 + j + 4,
                    ]
                )
        # Check columns
        for i in range(11):
            for j in range(15):
                myList.append(
                    [
                        (i) * 15 + j,
                        (i + 1) * 15 + j,
                        (i + 2) * 15 + j,
                        (i + 3) * 15 + j,
                        (i + 4) * 15 + j,
                    ]
                )
        # Check diagonals
        for i in range(11):
            for j in range(11):
                myList.append(
                    [
                        (i) * 15 + j,
                        (i + 1) * 15 + j + 1,
                        (i + 2) * 15 + j + 2,
                        (i + 3) * 15 + j + 3,
                        (i + 4) * 15 + j + 4,
                    ]
                )
        # Check diagonals (reverse)
        for i in range(11):
            for j in range(4, 15):
                myList.append(
                    [
                        (i) * 15 + j,
                        (i + 1) * 15 + j - 1,
                        (i + 2) * 15 + j - 2,
                        (i + 3) * 15 + j - 3,
                        (i + 4) * 15 + j - 4,
                    ]
                )
        return myList

    def is_win(self) -> bool:
        if self.__lastMove is None:
            return False

        lastMoveSymbol = TileType.WHITE if self.n_moves % 2 == 0 else TileType.BLACK
        width = 15
        board = self.board
        index = self.__lastMove
        row, col = divmod(index, width)

        directions = [
            (0, 1),  # Horizontal →
            (1, 0),  # Vertical ↓
            (1, 1),  # Diagonal ↘
            (1, -1),  # Diagonal ↙
        ]

        def check_line(row, col, dr, dc):
            count = 0
            for d in range(-4, 5):  # check from -4 to +4 steps
                r = row + dr * d
                c = col + dc * d
                if 0 <= r < width and 0 <= c < width:
                    idx = r * width + c
                    if board[idx] == lastMoveSymbol:
                        count += 1
                        if count == 5:
                            return True
                    else:
                        count = 0
                else:
                    count = 0
            return False

        for dr, dc in directions:
            if check_line(row, col, dr, dc):
                return True

        return False

    def is_draw(self) -> bool:
        return not self.is_win() and self.n_moves == 225

    def game_is_over(self) -> bool:
        return self.is_win() or self.is_draw()

    def moves(self) -> int:
        return self.n_moves

    def update_board(self, i) -> bool:
        if 0 <= i < 225 and self.board[i] == TileType.EMPTY:
            self.board[i] = TileType.BLACK if self.n_moves % 2 == 0 else TileType.WHITE
            self.n_moves += 1
            row, col = divmod(i, 15)

            self.corners[0] = min(self.corners[0], row - 1 if row > 0 else 0)
            self.corners[1] = min(self.corners[1], col - 1 if col > 0 else 0)
            self.corners[2] = max(self.corners[2], row + 1 if row < 14 else 14)
            self.corners[3] = max(self.corners[3], col + 1 if col < 14 else 14)
            self.__lastMove = i
            return True
        return False

    def reset(self, i: int) -> None:
        if 0 <= i < 225 and self.board[i] != TileType.EMPTY:
            self.board[i] = TileType.EMPTY
            self.n_moves -= 1
            self.__lastMove = None
        else:
            raise ValueError("Invalid position to reset.")

    def display_board(self) -> None:
        printableBoard = [
            "-" if i == TileType.EMPTY else "X" if i == TileType.BLACK else "O"
            for i in self.board
        ]
        for i in range(1, 16):
            print(f"{i:02}) ", end="")
            row = " ".join(printableBoard[(i - 1) * 15 : (i) * 15])
            print(row)

    def reset_board(self):
        self.board = [TileType.EMPTY] * 225
        self.corners = [50000, 50000, -50000, -50000]
        self.n_moves = 0
        self.__lastMove = None

    def heuristic(self) -> tuple[int, int]:
        blackScore: int = 0
        whiteScore: int = 0
        for winning_position in self.__winning_positions:
            total = 0
            for cell in winning_position:
                total += self.board[cell]
            if total == 0:
                continue
            if total % TileType.BLACK == 0:
                count = total // TileType.BLACK
                blackScore += count**count
            elif total % TileType.WHITE == 0:
                count = total // TileType.WHITE
                whiteScore += count**count
        return (blackScore, whiteScore)

    def set_corners(self, corners: list[int]):
        self.corners = corners.copy()

    def get_corners(self) -> list[int]:
        return self.corners.copy()
