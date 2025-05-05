class GomokuPlayer(Player):
    def get_move(self) -> tuple[int, int]:
        while True:
            try:
                move_input = input("Enter your move two numbers separated by space (row col, 0-14): ").strip()
                i, j = map(int, move_input.split())
                if 0 <= i < 15 and 0 <= j < 15:
                    return (i, j)
                else:
                    print("Invalid input: numbers must be between 0 and 14")
            except ValueError:
                print("Invalid input: please enter two numbers separated by space")
