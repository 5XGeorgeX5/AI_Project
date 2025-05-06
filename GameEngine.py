from GomokuBoard import GomokuBoard
from GomokuPlayer import GomokuPlayer
from structure import Player

class GameEngine:
    def __init__(self, player1: Player, player2: Player):
        self.board = GomokuBoard()
        self.players = (player1, player2)
        self.current_player_idx = 0

    def run(self):
        while not self.board.game_is_over():
            current_player = self.players[self.current_player_idx]
            self.board.display_board()
            print(f"Player {self.current_player_idx + 1}'s turn")

            while True:
                try:
                    i, j = current_player.get_move()
                    if self.board.update_board(i, j):
                        break
                    else:
                        print("Invalid move: Position already taken. Try again.")
                except ValueError as e:
                    print(e)

            if self.board.is_winner():
                self.board.display_board()
                print(f"Player {self.current_player_idx + 1} wins!")
                return
            
            self.current_player_idx = 1 - self.current_player_idx

        if self.board.is_draw():
            self.board.display_board()
            print("It's a draw!")

player1 = GomokuPlayer()
player2 = GomokuPlayer()

engine = GameEngine(player1, player2)
engine.run()