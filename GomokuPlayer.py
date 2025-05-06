from structure import Player

class GomokuPlayer(Player):
    def get_move(self) -> tuple[int, int]:
        while True:
            move_input = input("Enter your move (row col, 1-15, e.g., '7 7'): ").strip()
            
            if not move_input:
                print("Invalid input: Please enter two numbers separated by a space.")
                continue
            
            parts = move_input.split()
            
            if len(parts) != 2:
                print("Invalid input: Please enter exactly two numbers separated by a space.")
                continue
            
            try:
                i, j = map(int, parts)
            except ValueError:
                print("Invalid input: Both values must be integers.")
                continue
            
            if not (1 <= i < 16 and 1 <= j < 16):
                print("Invalid input: Numbers must be between 1 and 15.")
                continue
            
            return (i - 1, j - 1)