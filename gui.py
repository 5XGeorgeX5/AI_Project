import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QFrame

from GomokuBoard import GomokuBoard


# ======================
# Visual Board Widget
# ======================
class BoardWidget(QFrame):
    cell_size = 40
    move_made = pyqtSignal(int, int)

    def __init__(self, board, parent=None):
        super().__init__(parent)
        self.board = board
        self.setFixedSize(self.cell_size * 15, self.cell_size * 15)
        self.setStyleSheet("background-color: #deb887;")

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_board(painter)
        self.draw_stones(painter)

    def draw_board(self, painter):
        for i in range(15):
            painter.drawLine(i * self.cell_size, 0, i * self.cell_size, 15 * self.cell_size)
            painter.drawLine(0, i * self.cell_size, 15 * self.cell_size, i * self.cell_size)

    def draw_stones(self, painter):
        for i in range(225):
            row = i // 15
            col = i % 15
            stone = self.board.board[i]
            if stone == 'X':
                self.draw_stone(painter, col, row, Qt.black)
            elif stone == 'O':
                self.draw_stone(painter, col, row, Qt.white)

    def draw_stone(self, painter, x, y, color):
        painter.setBrush(QBrush(color, Qt.SolidPattern))
        painter.drawEllipse(
            x * self.cell_size + 5,
            y * self.cell_size + 5,
            self.cell_size - 10,
            self.cell_size - 10
        )

    def mousePressEvent(self, event):
        col = event.x() // self.cell_size
        row = event.y() // self.cell_size
        if 0 <= row < 15 and 0 <= col < 15:
            self.move_made.emit(row, col)

# ======================
# Game Execution Thread
# ======================
class GameThread(QThread):
    game_over_signal = pyqtSignal(str)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    def run(self):
        # TODO: Implement game logic using the GameEngine
        pass

# ======================
# Main GUI Window
# ======================
class GomokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.board_widget = None
        self.selected_mode = None
        self.human_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gomoku Game")
        layout = QVBoxLayout()
        self.label = QLabel("Choose Game Mode", self)
        layout.addWidget(self.label)

        self.ai_vs_ai_button = QPushButton("AI vs AI (MiniMax vs AlphaBeta)", self)
        self.ai_vs_ai_button.clicked.connect(self.select_ai_vs_ai)
        layout.addWidget(self.ai_vs_ai_button)

        self.human_vs_minimax_button = QPushButton("Human vs MiniMax AI", self)
        self.human_vs_minimax_button.clicked.connect(self.select_human_vs_minimax)
        layout.addWidget(self.human_vs_minimax_button)

        self.human_vs_alphabeta_button = QPushButton("Human vs AlphaBeta AI", self)
        self.human_vs_alphabeta_button.clicked.connect(self.select_human_vs_alphabeta)
        layout.addWidget(self.human_vs_alphabeta_button)

        self.human_vs_human_button = QPushButton("Human vs Human", self)
        self.human_vs_human_button.clicked.connect(self.select_human_vs_human)
        layout.addWidget(self.human_vs_human_button)

        self.start_button = QPushButton("Start Game", self)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def select_ai_vs_ai(self):
        self.selected_mode = "ai_vs_ai"
        QMessageBox.information(self, "Selection", "AI vs AI mode selected.")

    def select_human_vs_minimax(self):
        self.selected_mode = "human_vs_minimax"
        QMessageBox.information(self, "Selection", "Human vs MiniMax AI mode selected.")

    def select_human_vs_alphabeta(self):
        self.selected_mode = "human_vs_alphabeta"
        QMessageBox.information(self, "Selection", "Human vs AlphaBeta AI mode selected.")

    def select_human_vs_human(self):
        self.selected_mode = "human_vs_human"
        QMessageBox.information(self, "Selection", "Human vs Human mode selected.")

    def start_game(self):
        if not self.selected_mode:
            QMessageBox.warning(self, "Warning", "Please select a game mode before starting the game.")
            return

        board = GomokuBoard()  # TODO: Initialize the board
        try:
            if self.selected_mode == "ai_vs_ai":
                # TODO: Initialize AI players and start the game
                pass

            elif self.selected_mode in ["human_vs_minimax", "human_vs_alphabeta"]:
                # TODO: Initialize human player and AI player, and start the game
                pass

            elif self.selected_mode == "human_vs_human":
                # TODO: Initialize two human players and start the game
                pass

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def human_move(self, row, col):
        # TODO: Implement human move logic
        pass

    def ai_move(self):
        # TODO: Implement AI move logic
        pass

    def show_result(self, result):
        # TODO: Implement result display logic
        pass

# ======================
# App Entry Point
# ======================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GomokuGUI()
    gui.resize(300, 200)
    gui.show()
    sys.exit(app.exec_())