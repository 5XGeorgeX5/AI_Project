import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QCheckBox,
    QComboBox,
)


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
                            print("file input.txt contains an invalid input")
                            sys.exit(1)
        except IOError:
            print("Error opening the file input.txt!")
            sys.exit(1)

        if x_count - o_count > 1 or o_count > x_count:
            print("file input.txt contains an invalid input")
            sys.exit(1)
        if len(matrix) != 225:  # 15 x 15
            print("file input.txt contains an invalid input")
            sys.exit(1)
        self.board = matrix
        self.n_moves = x_count + o_count
        if self.n_moves == 225:
            print("Input can't be a finished game")
            sys.exit(1)
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
                print("Input can't be a finished game: 5 in a row detected.")
                sys.exit(1)
        self.__scores[0] = blackScore
        self.__scores[1] = whiteScore

    def is_draw(self) -> bool:
        return not self.is_win() and self.n_moves == 225

    def game_is_over(self) -> bool:
        return self.is_win() or self.is_draw()

    def moves(self) -> int:
        return self.n_moves

    def is_valid_move(self, i: int) -> bool:
        return 0 <= i < 225 and self.board[i] == TileType.EMPTY

    def update_board(self, i) -> None:
        oldScores = self.getTileScores(i)
        self.__scores[0] -= oldScores[0]
        self.__scores[1] -= oldScores[1]

        self.board[i] = TileType.BLACK if self.n_moves % 2 == 0 else TileType.WHITE
        self.n_moves += 1
        self.__lastMove = i
        newScores = self.getTileScores(i)
        self.__scores[0] += newScores[0]
        self.__scores[1] += newScores[1]

        row, col = divmod(i, 15)

        self.corners[0] = min(self.corners[0], row - 2 if row > 1 else 0)
        self.corners[1] = min(self.corners[1], col - 2 if col > 1 else 0)
        self.corners[2] = max(self.corners[2], row + 2 if row < 13 else 14)
        self.corners[3] = max(self.corners[3], col + 2 if col < 13 else 14)

    def reset(self, i: int) -> None:
        oldScores = self.getTileScores(i)
        self.__scores[0] -= oldScores[0]
        self.__scores[1] -= oldScores[1]

        self.board[i] = TileType.EMPTY
        self.n_moves -= 1
        self.__lastMove = None

        newScores = self.getTileScores(i)
        self.__scores[0] += newScores[0]
        self.__scores[1] += newScores[1]

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
                    self.corners[0] = min(self.corners[0], i - 2 if i > 1 else 0)
                    self.corners[1] = min(self.corners[1], j - 2 if j > 1 else 0)
                    self.corners[2] = max(self.corners[2], i + 2 if i < 13 else 14)
                    self.corners[3] = max(self.corners[3], j + 2 if j < 13 else 14)


class Player:
    def __init__(self, name: str = "Player"):
        self.name = name

    def get_move(self) -> int:
        raise NotImplementedError


class GomokuPlayer(Player):
    def __init__(self):
        self.name = "Human"

    def get_move(self) -> int:
        while True:
            move_input = input("Enter your move (row col, 1-15, e.g., '8 8'): ").strip()

            if not move_input:
                print("Invalid input: Please enter two numbers separated by a space.")
                continue

            parts = move_input.split()

            if len(parts) != 2:
                print(
                    "Invalid input: Please enter exactly two numbers separated by a space."
                )
                continue

            try:
                i, j = map(int, parts)
            except ValueError:
                print("Invalid input: Both values must be integers.")
                continue

            if not (1 <= i < 16 and 1 <= j < 16):
                print("Invalid input: Numbers must be between 1 and 15.")
                continue

            return (i - 1) * 15 + (j - 1)


class BaseAIPlayer(Player):

    def __init__(self, board: GomokuBoard):
        self.board = board
        self.runs = 0

    def valideMoves(self) -> list:
        corners = self.board.get_corners()
        start = corners[0] * 15 + corners[1]
        end = corners[2] * 15 + corners[3]
        length = corners[3] - corners[1] + 1
        moves = []
        while start < end:
            for j in range(start, start + length):
                if self.board.is_valid_move(j):
                    self.board.update_board(j)
                    blackScore, whiteScore = self.board.heuristic()
                    moves.append((blackScore - whiteScore, j))
                    self.board.reset(j)
            start += 15
        self.board.set_corners(corners)
        # if black turn -> sort descending
        moves.sort(reverse=(self.board.moves() % 2 == 0))
        return moves[:40]


class MiniMaxAIPlayer(BaseAIPlayer):
    __depth = 2
    __isBlack = None

    def __init__(self, board: GomokuBoard, depth: int = 2):
        super().__init__(board)
        self.__depth = depth
        self.name = "MiniMax"

    def minimax(self, maximizingPlayer: bool, depth: int) -> int:
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
                value = self.minimax(False, depth - 1)
                self.board.reset(move)
                self.board.set_corners(corners)
                maxEval = max(maxEval, value)
            return maxEval
        else:
            minEval = 500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(True, depth - 1)
                self.board.reset(move)
                self.board.set_corners(corners)
                minEval = min(minEval, value)
            return minEval

    def get_move(self) -> int:
        self.__isBlack = (self.board.moves() % 2) == 0
        if self.board.moves() == 0:
            return 112  # position 8, 8
        index = -1
        corners = self.board.get_corners()

        moves = self.valideMoves()

        if self.__isBlack:
            maxEval = -500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(False, self.__depth - 1)
                self.board.reset(move)
                self.board.set_corners(corners)
                if value > maxEval:
                    index = move
                    maxEval = value
        else:
            minEval = 500000000
            for _, move in moves:
                self.board.update_board(move)
                value = self.minimax(True, self.__depth - 1)
                self.board.reset(move)
                self.board.set_corners(corners)
                if value < minEval:
                    index = move
                    minEval = value
        return index


class AlphaBetaAIPlayer(BaseAIPlayer):
    __depth = 2
    __isBlack = None

    def __init__(self, board: GomokuBoard, depth: int = 2):
        super().__init__(board)
        self.__depth = depth
        self.name = "AlphaBeta"

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
                    beta = value
        return index


########### FOR RUNNING IN TERMINAL ###########
###############################################
class GameEngine:
    def __init__(self, player1: Player, player2: Player, board: GomokuBoard):
        self.board = board
        self.players = (player1, player2)
        self.current_player_idx = board.moves() % 2

    def run(self):
        while not self.board.game_is_over():
            current_player = self.players[self.current_player_idx]
            self.board.display_board()
            print(f"Player {self.current_player_idx + 1}'s turn")

            while True:
                i = current_player.get_move()
                if self.board.is_valid_move(i):
                    break
                else:
                    print("Invalid move: Position already taken. Try again.")

            self.board.update_board(i)

            if self.board.is_win():
                self.board.display_board()
                print(f"Player {self.current_player_idx + 1} wins!")
                return

            self.current_player_idx = 1 - self.current_player_idx

        self.board.display_board()
        print("It's a draw!")


###############################################
###############################################
# ======================
# Visual Board Widget
# ======================
class GomokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gomoku - Choose Game Mode")
        self.setFixedSize(600, 250)

        layout = QVBoxLayout()

        self.label1 = QLabel("Select Player 1 (Black):", self)
        self.combo1 = QComboBox(self)
        self.combo1.addItems(["Human", "MiniMax", "AlphaBeta"])

        self.label2 = QLabel("Select Player 2 (White):", self)
        self.combo2 = QComboBox(self)
        self.combo2.addItems(["Human", "MiniMax", "AlphaBeta"])

        self.read_board_input = QCheckBox("Read board from input.txt file", self)
        self.read_board_input.setChecked(False)

        # Start button
        self.start_button = QPushButton("Start Game", self)
        self.start_button.clicked.connect(self.start_game)

        layout.addWidget(self.label1)
        layout.addWidget(self.combo1)
        layout.addWidget(self.label2)
        layout.addWidget(self.combo2)
        layout.addWidget(self.read_board_input)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_game(self):
        self.board = GomokuBoard(readBoardInput=self.read_board_input.isChecked())
        player1_type = self.combo1.currentText()
        player2_type = self.combo2.currentText()

        def create_player(playerType: str) -> Player:
            if playerType == "Human":
                return GomokuPlayer()
            elif playerType == "MiniMax":
                return MiniMaxAIPlayer(self.board, depth=2)
            elif playerType == "AlphaBeta":
                return AlphaBetaAIPlayer(self.board, depth=3)

        player1 = create_player(player1_type)
        player2 = create_player(player2_type)

        self.game_window = GameWindow(player1, player2, self.board, self)
        self.game_window.show()
        self.hide()


class GameWindow(QWidget):
    def __init__(
        self, player1: Player, player2: Player, board: GomokuBoard, parent: GomokuGUI
    ):
        super().__init__()
        self.board = board
        self.players = (player1, player2)
        self.setWindowTitle("Gomoku Game")
        self.setFixedSize(640, 700)
        self.cell_size = 40
        self.margin = 20
        self.current_player_idx = self.board.moves() % 2
        self.delay = 100
        self.setStyleSheet("background-color: #deb887;")
        self.menu = parent

        # Status label
        self.status_label = QLabel(
            f"Player {self.current_player_idx + 1}'s Turn: {self.players[self.current_player_idx].name}",
            self,
        )
        self.status_label.setGeometry(20, 625, 600, 30)

        # Reset Button
        self.reset_button = QPushButton("Reset Game", self)
        self.reset_button.setGeometry(20, 660, 120, 30)
        self.reset_button.clicked.connect(self.reset_game)

        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(150, 660, 120, 30)
        self.back_button.clicked.connect(self.back_to_menu)

        # AI move timer
        if isinstance(self.players[self.current_player_idx], BaseAIPlayer):
            QTimer.singleShot(self.delay, self.make_ai_move)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_board(painter)
        self.draw_pieces(painter)

    def draw_board(self, painter):
        painter.setPen(Qt.black)
        for row in range(16):
            painter.drawLine(
                self.margin,
                self.margin + row * self.cell_size,
                self.margin + 15 * self.cell_size,
                self.margin + row * self.cell_size,
            )
        for col in range(16):
            painter.drawLine(
                self.margin + col * self.cell_size,
                self.margin,
                self.margin + col * self.cell_size,
                self.margin + 15 * self.cell_size,
            )

    def draw_pieces(self, painter):
        for i in range(225):
            row, col = divmod(i, 15)
            x = self.margin + col * self.cell_size
            y = self.margin + row * self.cell_size
            if self.board.board[i] == TileType.BLACK:
                painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
                painter.drawEllipse(
                    x + 5, y + 5, self.cell_size - 10, self.cell_size - 10
                )
            elif self.board.board[i] == TileType.WHITE:
                painter.setPen(Qt.black)
                painter.setBrush(Qt.white)
                painter.drawEllipse(
                    x + 5, y + 5, self.cell_size - 10, self.cell_size - 10
                )

    def mousePressEvent(self, event):
        if self.board.game_is_over():
            return

        current_player = self.players[self.current_player_idx]
        if isinstance(current_player, GomokuPlayer):  # Human player
            x = event.x() - self.margin
            y = event.y() - self.margin
            if 0 <= x < 15 * self.cell_size and 0 <= y < 15 * self.cell_size:
                col = x // self.cell_size
                row = y // self.cell_size
                index = row * 15 + col
                self.handle_human_move(index)

    def handle_human_move(self, index):
        if not self.board.is_valid_move(index):
            return
        self.board.update_board(index)
        self.update()
        self.check_game_status()

        if not self.board.game_is_over():
            self.current_player_idx = 1 - self.current_player_idx
            self.status_label.setText(
                f"Player {self.current_player_idx + 1}'s Turn: {self.players[self.current_player_idx].name}"
            )
            if isinstance(self.players[self.current_player_idx], BaseAIPlayer):
                QTimer.singleShot(self.delay, self.make_ai_move)

    def make_ai_move(self):
        ai_player = self.players[self.current_player_idx]
        move = ai_player.get_move()
        self.board.update_board(move)
        self.update()
        self.check_game_status()

        if not self.board.game_is_over():
            self.current_player_idx = 1 - self.current_player_idx
            self.status_label.setText(
                f"Player {self.current_player_idx + 1}'s Turn: {self.players[self.current_player_idx].name}"
            )
            if isinstance(self.players[self.current_player_idx], BaseAIPlayer):
                QTimer.singleShot(self.delay, self.make_ai_move)

    def check_game_status(self):
        if self.board.is_win():
            winner = self.current_player_idx + 1
            QMessageBox.information(self, "Game Over", f"Player {winner} wins!")
        elif self.board.is_draw():
            QMessageBox.information(self, "Game Over", "It's a draw!")

    def reset_game(self):
        self.board.reset_board()
        self.current_player_idx = self.board.moves() % 2
        self.status_label.setText(
            f"Player {self.current_player_idx + 1}'s Turn: {self.players[self.current_player_idx].name}"
        )
        self.update()
        if isinstance(self.players[self.current_player_idx], BaseAIPlayer):
            QTimer.singleShot(self.delay, self.make_ai_move)

    def back_to_menu(self):
        self.menu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GomokuGUI()
    gui.show()
    sys.exit(app.exec_())


"""
the input file input.txt should be in the same directory as this file
the input file should contain the board in the following format:
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - X - - - - - - - -
- - - - - O O X - - - - - - -
- - - X X O O O X - - - - - -
- - - X X X O X - O - - - - -
- - - - - - X - - - - - - - -
- - - - - O - O - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
- - - - - - - - - - - - - - -
"""
