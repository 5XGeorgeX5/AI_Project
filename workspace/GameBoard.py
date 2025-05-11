SIZE = 15

class TileType:
    EMPTY = 0
    BLACK = 7
    WHITE = 11
def read_game_board():
    matrix = []
    x_count = 0
    o_count = 0
    try:
        with open("input.txt", "r") as input_file:
            for line in input_file:
                for c in line:
                    if c.isspace():
                        continue
                    if c == 'X':
                        matrix.append(TileType.BLACK)
                        x_count += 1
                    elif c == 'O':
                        matrix.append(TileType.WHITE)
                        o_count += 1
                    elif c == '-':
                        matrix.append(TileType.EMPTY)
                    else:
                        pass
    except IOError:
        print("Error opening file!")
        return None

    if abs(x_count - o_count) > 1:
        print("This is an invalid input")
        return None
    while len(matrix) < SIZE * SIZE:
        matrix.append(TileType.EMPTY)
    matrix = matrix[:SIZE*SIZE]
    return matrix

