import numpy as np

# Define shift directions
N = +8
S = -8
W = +1
E = -1
NE = N + E
SE = S + E
NW = N + W
SW = S + W


def print_bit_board(bit_board):
    string = ""
    for row in range(8):
        for col in range(8):
            string = str((bit_board >> (col + 8*row)) & 1) + string
        string = "\n" + string
    print(string[1:])


def shift(bb, direction):
    return bb << direction


def v_flip(bb):
    return \
            (bb << 56) |\
            ((bb << 40) & 0x00ff000000000000) |\
            ((bb << 24) & 0x0000ff0000000000) |\
            ((bb << 8) & 0x000000ff00000000) |\
            ((bb >> 8) & 0x00000000ff000000) |\
            ((bb >> 24) & 0x0000000000ff0000) |\
            ((bb >> 40) & 0x000000000000ff00) |\
            (bb >> 56)


def LS1B(bb):
    return bb & -bb


def reset_LS1B(bb):
    return bb & (bb-1)


def population_count(bb):
    count = 0
    while bb:
        count += 1
        bb &= bb - 1
    return count


index64 = [
    0, 47,  1, 56, 48, 27,  2, 60,
    57, 49, 41, 37, 28, 16,  3, 61,
    54, 58, 35, 52, 50, 42, 21, 44,
    38, 32, 29, 23, 17, 11,  4, 62,
    46, 55, 26, 59, 40, 36, 15, 53,
    34, 51, 20, 43, 31, 22, 10, 45,
    25, 39, 14, 33, 19, 30,  9, 24,
    13, 18,  8, 12,  7,  6,  5, 63
]

debruijn64 = np.int64(0x03f79d71b4cb0a89)


def bitScanForward(bb):
    assert bb != 0
    return index64[(np.multiply(bb ^ (bb-1), debruijn64, dtype=np.int64)) >> 58]


def get_indices(bb):
    indices = []
    while bb:
        indices.append(bitScanForward(bb))
        bb = reset_LS1B(bb)

    return indices
