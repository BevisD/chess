def print_bit_board(bit_board):
    string = ""
    for row in range(8):
        for col in range(8):
            string = str((bit_board >> (col + 8*row)) & 1) + string
        string = "\n" + string
    print(string[1:])
