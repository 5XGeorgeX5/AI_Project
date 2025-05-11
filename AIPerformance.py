from GomokuBoard import GomokuBoard, TileType
from GomokuPlayer import GomokuPlayer
from structure import Player
from MinimaxAIPlayer import MiniMaxAIPlayer
from AlphaBetaAIPlayer import AlphaBetaAIPlayer
import time


def test(player1: Player, player2: Player, board: GomokuBoard):
    averages = [0.0, 0.0]
    maxes = [0.0, 0.0]
    mins = [float("inf"), float("inf")]
    players = (player1, player2)
    current_player_idx = board.moves() % 2
    file = open("performance.txt", "a")

    total_time_start = time.perf_counter()

    while True:
        current_player = players[current_player_idx]
        board.display_board()
        print()

        start = time.perf_counter()
        i = current_player.get_move()
        end = time.perf_counter()
        elapsed_time = end - start
        averages[current_player_idx] += elapsed_time
        maxes[current_player_idx] = max(maxes[current_player_idx], elapsed_time)
        mins[current_player_idx] = min(mins[current_player_idx], elapsed_time)
        if not board.update_board(i):
            print(f"Invalid move {i} from Player {current_player_idx + 1}")
            return

        if board.is_win():
            board.display_board()
            print(f"Player {current_player_idx + 1} wins!")
            file.write(f"Player {current_player_idx + 1} wins!\n")
            break
        elif board.is_draw():
            board.display_board()
            print("It's a draw!")
            file.write("It's a draw!\n")
            break

        current_player_idx = 1 - current_player_idx
    total_time_end = time.perf_counter()
    total_elapsed_time = total_time_end - total_time_start
    file.write(f"Total time: {total_elapsed_time:.6f} seconds\n\n")

    averages[0] /= (board.moves() + 1) // 2
    averages[1] /= board.moves() // 2

    file.write("Player 1:\n")
    file.write(f"Average time: {averages[0]:.6f} seconds\n")
    file.write(f"Max time: {maxes[0]:.6f} seconds\n")
    file.write(f"Min time: {mins[0]:.6f} seconds\n")
    file.write(f"Runs: {player1.runs}\n\n")

    file.write("Player 2:\n")
    file.write(f"Average time: {averages[1]:.6f} seconds\n")
    file.write(f"Max time: {maxes[1]:.6f} seconds\n")
    file.write(f"Min time: {mins[1]:.6f} seconds\n")
    file.write(f"Runs: {player2.runs}\n\n")
    printableBoard = [
        "-" if i == TileType.EMPTY else "X" if i == TileType.BLACK else "O"
        for i in board.board
    ]
    for i in range(1, 16):
        file.write(f"{i:02}) ")
        row = " ".join(printableBoard[(i - 1) * 15 : (i) * 15])
        file.write(row)
        file.write("\n")
    file.write("\n==========================================\n\n")
    file.close()


board = GomokuBoard()
player1 = AlphaBetaAIPlayer(board)
player2 = AlphaBetaAIPlayer(board)

test(player1, player2, board)
