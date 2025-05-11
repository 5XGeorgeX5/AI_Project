class TileType:
    EMPTY = 0
    BLACK = 7
    WHITE = 11


class GomokuBoard:
    __lastMove = None
    __winning_positions_dict = None
    __scores = [0, 0]

    def __init__(self, readBoardInput: bool = False):
        if readBoardInput:
            self.read_board_input()
        else:
            self.board = [TileType.EMPTY] * 225
            self.n_moves = 0
            # [start row, start colm, end row , end colm]
            self.corners = [50000, 50000, -50000, -50000]

        self.__winning_positions_dict = self.get_winning_positions_dict()

    def read_board_input(self):
        matrix = []
        x_count = 0
        o_count = 0
        try:
            with open("input.txt", "r") as input_file:
                for line in input_file:
                    for c in line:
                        if c.isspace():
                            continue
                        if c == "X":
                            matrix.append(TileType.BLACK)
                            x_count += 1
                        elif c == "O":
                            matrix.append(TileType.WHITE)
                            o_count += 1
                        elif c == "-":
                            matrix.append(TileType.EMPTY)
                        else:
                            raise ValueError(f"invalide character: {c}")
        except IOError:
            raise IOError("Error opening file!")

        if x_count - o_count > 1 or o_count > x_count:
            raise ValueError("This is an invalid input")
        if len(matrix) != 225:  # 15 x 15
            raise ValueError("This is an invalid input")
        self.board = matrix
        self.n_moves = x_count + o_count
        if self.n_moves == 225:
            raise ValueError("Input can't be a finished game")
        self.initalizeHeuristic()
        self.initalizeCorners()

    def get_winning_positions(self) -> list[tuple[int, ...]]:
        winning_positions: list[tuple[int, ...]] = []

        # Rows
        for i in range(15):
            for j in range(11):
                pos = [i * 15 + j + k for k in range(5)]
                winning_positions.append(tuple(pos))

        # Columns
        for i in range(11):
            for j in range(15):
                pos = [(i + k) * 15 + j for k in range(5)]
                winning_positions.append(tuple(pos))

        # Diagonals (top-left to bottom-right)
        for i in range(11):
            for j in range(11):
                pos = [(i + k) * 15 + j + k for k in range(5)]
                winning_positions.append(tuple(pos))

        # Diagonals (top-right to bottom-left)
        for i in range(11):
            for j in range(4, 15):
                pos = [(i + k) * 15 + j - k for k in range(5)]
                winning_positions.append(tuple(pos))

        return winning_positions

    def get_winning_positions_dict(self) -> tuple[list[tuple[int, ...]]]:
        winning_dict = tuple([] for _ in range(225))
        winning_positions = self.get_winning_positions()
        for pos in winning_positions:
            for idx in pos:
                winning_dict[idx].append(pos)
        return winning_dict

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

    def getTileScores(self, tile):
        blackScore = 0
        whiteScore = 0
        for winning_position in self.__winning_positions_dict[tile]:
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

    def heuristic(self) -> tuple[int, int]:
        return tuple(self.__scores)

    def initalizeHeuristic(self) -> None:
        self.__scores = [0, 0]
        winning_positions = self.get_winning_positions()
        blackScore = 0
        whiteScore = 0
        for winning_position in winning_positions:
            total = 0
            count = 0
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
            if count == 5:
                raise ValueError("Input can't be a finished game: 5 in a row detected.")
        self.__scores[0] = blackScore
        self.__scores[1] = whiteScore

    def is_draw(self) -> bool:
        return not self.is_win() and self.n_moves == 225

    def game_is_over(self) -> bool:
        return self.is_win() or self.is_draw()

    def moves(self) -> int:
        return self.n_moves

    def update_board(self, i) -> bool:
        if 0 <= i < 225 and self.board[i] == TileType.EMPTY:
            oldScores = self.getTileScores(i)
            self.__scores[0] -= oldScores[0]
            self.__scores[1] -= oldScores[1]

            self.board[i] = TileType.BLACK if self.n_moves % 2 == 0 else TileType.WHITE
            self.n_moves += 1
            row, col = divmod(i, 15)

            self.corners[0] = min(self.corners[0], row - 1 if row > 0 else 0)
            self.corners[1] = min(self.corners[1], col - 1 if col > 0 else 0)
            self.corners[2] = max(self.corners[2], row + 1 if row < 14 else 14)
            self.corners[3] = max(self.corners[3], col + 1 if col < 14 else 14)

            self.__lastMove = i

            newScores = self.getTileScores(i)
            self.__scores[0] += newScores[0]
            self.__scores[1] += newScores[1]
            return True
        return False

    def reset(self, i: int) -> None:
        if 0 <= i < 225 and self.board[i] != TileType.EMPTY:
            oldScores = self.getTileScores(i)
            self.__scores[0] -= oldScores[0]
            self.__scores[1] -= oldScores[1]

            self.board[i] = TileType.EMPTY
            self.n_moves -= 1
            self.__lastMove = None

            newScores = self.getTileScores(i)
            self.__scores[0] += newScores[0]
            self.__scores[1] += newScores[1]
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
        self.__scores = [0, 0]

    def set_corners(self, corners: list[int]):
        self.corners = corners.copy()

    def get_corners(self) -> list[int]:
        return self.corners.copy()

    def initalizeCorners(self) -> None:
        self.corners = [50000, 50000, -50000, -50000]
        for i in range(15):
            for j in range(15):
                if self.board[i * 15 + j] != TileType.EMPTY:
                    self.corners[0] = min(self.corners[0], i - 1 if i > 0 else 0)
                    self.corners[1] = min(self.corners[1], j - 1 if j > 0 else 0)
                    self.corners[2] = max(self.corners[2], i + 1 if i < 14 else 14)
                    self.corners[3] = max(self.corners[3], j + 1 if j < 14 else 14)
