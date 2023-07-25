from bitboard import *
from initboard import *
from GUI import *


def single_push_targets(pawns: int, empty: int, colour: int):
    push_targets = ((pawns << 8) >> (colour << 4)) & empty
    return push_targets


def pawn_west_attacks(pawns: int, attackable: int, colour: int):
    pawns &= NOT_A_FILE
    west_attacks = ((pawns << 9) >> (colour << 4)) & attackable
    return west_attacks


def pawn_east_attacks(pawns: int, attackable: int, colour: int):
    pawns &= NOT_H_FILE
    east_attacks = ((pawns << 7) >> (colour << 4)) & attackable
    return east_attacks


class ChessBoard:
    def __init__(self):
        self.king_list = [W_KING, B_KING]
        self.queens_list = [W_QUEEN, B_QUEEN]
        self.bishops_list = [W_BISHOPS, B_BISHOPS]
        self.knights_list = [W_KNIGHTS, B_KNIGHTS]
        self.rooks_list = [W_ROOKS, B_ROOKS]
        self.pawns_list = [W_PAWNS, B_PAWNS]
        self.pieces_list = [W_PIECES, B_PIECES]
        self.pieces = self.pieces_list[0] | self.pieces_list[1]
        self.empty = ~self.pieces
        self.en_passant = 0

    def legal_moves(self, colour: int):
        moves = []
        moves += self.legal_king_moves(colour)
        moves += self.legal_queen_moves(colour)
        moves += self.legal_bishop_moves(colour)
        moves += self.legal_knight_moves(colour)
        moves += self.legal_rook_moves(colour)
        moves += self.legal_pawn_moves(colour)

        return moves

    def legal_king_moves(self, colour: int):
        return []

    def legal_queen_moves(self, colour: int):
        return []

    def legal_bishop_moves(self, colour: int):
        return []

    def legal_knight_moves(self, colour: int):
        return []

    def legal_rook_moves(self, colour: int):
        return []

    def legal_pawn_moves(self, colour: int):
        moves = []
        moves += self.legal_single_push_moves(colour)
        moves += self.legal_double_push_moves(colour)
        moves += self.legal_attack_moves(colour)
        return moves

    def legal_single_push_moves(self, colour: int):
        moves = []
        push_targets = single_push_targets(self.pawns_list[colour],
                                           self.empty, colour)
        indices = get_indices(push_targets)

        for to_square in indices:
            if colour:
                from_square = to_square+8
            else:
                from_square = to_square-8

            if to_square >= 56 or to_square <= 7:
                for code in range(8, 12):
                    moves.append((code, to_square, from_square))
            else:
                moves.append((0, to_square, from_square))
        return moves

    def legal_double_push_moves(self, colour: int):
        moves = []
        single_pawn_targets = single_push_targets(self.pawns_list[colour],
                                                  self.empty, colour)
        double_push_targets = single_push_targets(single_pawn_targets,
                                                  self.empty, colour)
        indices = get_indices(double_push_targets)

        for to_square in indices:
            from_square = to_square - 16

            moves.append((0, to_square, from_square))
        return moves

    def legal_attack_moves(self, colour):
        moves = []
        west_attacks = pawn_west_attacks(self.pawns_list[colour],
                                         self.pieces_list[~colour], colour)
        east_attacks = pawn_east_attacks(self.pawns_list[colour],
                                         self.pieces_list[~colour], colour)
        west_en_passant = pawn_west_attacks(self.pawns_list[colour],
                                            self.en_passant, colour)
        east_en_passant = pawn_east_attacks(self.pawns_list[colour],
                                            self.en_passant, colour)

        west_indices = get_indices(west_attacks)
        east_indices = get_indices(east_attacks)
        west_en_passant_indices = get_indices(west_en_passant)
        east_en_passant_indices = get_indices(east_en_passant)

        west_offset = -7 if colour else 9
        east_offset = -9 if colour else 7

        west_moves = [(4, to_square, to_square - west_offset)
                      for to_square in west_indices]
        east_moves = [(4, to_square, to_square - east_offset)
                      for to_square in east_indices]
        west_en_passant_moves = [(5, to_square, to_square - west_offset)
                                 for to_square in west_en_passant_indices]
        east_en_passant_moves = [(5, to_square, to_square - east_offset)
                                 for to_square in east_en_passant_indices]

        for move in west_moves + east_moves + \
                    west_en_passant_moves + east_en_passant_moves:
            to_square = move[1]
            from_square = move[2]
            if to_square >= 56 or to_square <= 7:
                for code in range(12, 16):
                    moves.append((code, to_square, from_square))
            else:
                moves.append(move)

        return moves


