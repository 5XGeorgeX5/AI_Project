class TileType:
    EMPTY = 0
    BLACK = 7
    WHITE = 11


class GomokuBoard:
    __lastMove = None
    __winning_positions_dict = None
    __scores = [0, 0]

    def __init__(self):
        self.board = [TileType.EMPTY] * 225
        self.n_moves = 0
        self.corners = [
            50000,
            50000,
            -50000,
            -50000,
        ]  # [start row, start colm, end row , end colm]
        self.__winning_positions_dict = self.get_winning_positions_dict()

    def get_winning_positions_dict(self) -> dict[int, list[tuple[int, ...]]]:
        winning_dict: dict[int, list[tuple[int, ...]]] = {}

        def add_position(pos: tuple[int, ...]):
            pos_tuple = tuple(pos)
            for idx in pos:
                if idx not in winning_dict:
                    winning_dict[idx] = []
                winning_dict[idx].append(pos_tuple)

        # Rows
        for i in range(15):
            for j in range(11):
                pos = [i * 15 + j + k for k in range(5)]
                add_position(pos)

        # Columns
        for i in range(11):
            for j in range(15):
                pos = [(i + k) * 15 + j for k in range(5)]
                add_position(pos)

        # Diagonals (top-left to bottom-right)
        for i in range(11):
            for j in range(11):
                pos = [(i + k) * 15 + j + k for k in range(5)]
                add_position(pos)

        # Diagonals (top-right to bottom-left)
        for i in range(11):
            for j in range(4, 15):
                pos = [(i + k) * 15 + j - k for k in range(5)]
                add_position(pos)

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
