from bitboard import *
from constants import *


def single_push_targets(pawns: int, empty: int, colour: int):
    push_targets = ((pawns << 8) >> (colour << 4)) & empty
    return push_targets


def pawn_west_attacks(pawns: int, attackable: int, colour: int):
    pawns &= NOT_A_FILE_BB
    west_attacks = ((pawns << 9) >> (colour << 4)) & attackable
    return west_attacks


def pawn_east_attacks(pawns: int, attackable: int, colour: int):
    pawns &= NOT_H_FILE_BB
    east_attacks = ((pawns << 7) >> (colour << 4)) & attackable
    return east_attacks


class ChessBoard:
    def __init__(self):
        self.bitboards = [[W_KING_BB, W_QUEEN_BB, W_ROOKS_BB, W_BISHOPS_BB, W_KNIGHTS_BB, W_PAWNS_BB],
                          [B_KING_BB, B_QUEEN_BB, B_ROOKS_BB, B_BISHOPS_BB, B_KNIGHTS_BB, B_PAWNS_BB]]
        self.en_passant = 0
        self.pieces = [self.get_piece_bitboard(WHITE),
                       self.get_piece_bitboard(BLACK)]

        self.all_pieces = self.pieces[WHITE] | self.pieces[WHITE]
        self.empty = ~self.all_pieces

        self.turn = WHITE
        self.move_list = self.legal_moves(WHITE)

    def get_piece_bitboard(self, colour):
        pieces = 0
        for bitboard in self.bitboards[colour]:
            pieces |= bitboard
        return pieces

    def make_move(self, move):
        code, to_square, from_square = move
        # TODO Move making must be easily un-doable for min-max

        # QUIET MOVE
        if code == 0:
            mask = (0b1 << to_square) + (0b1 << from_square)
            for piece, bitboard in enumerate(self.bitboards[self.turn]):
                if mask & bitboard:
                    self.bitboards[self.turn][piece] ^= mask
                    break

        # DOUBLE-PUSH
        elif code == 1:
            mask = (0b1 << to_square) + (0b1 << from_square)
            for piece, bitboard in enumerate(self.bitboards[self.turn]):
                if mask & bitboard:
                    self.bitboards[self.turn][piece] ^= mask
                    break
            if self.turn == WHITE:
                self.en_passant = 0b1 << (from_square + 8)
            else:
                self.en_passant = 0b1 << (from_square - 8)

        # KING-CASTLE
        elif code == 2:
            pass

        # QUEEN-CASTLE
        elif code == 3:
            pass

        # CAPTURE
        elif code == 4:
            move_mask = (0b1 << to_square) + (0b1 << from_square)
            for piece, bitboard in enumerate(self.bitboards[self.turn]):
                if move_mask & bitboard:
                    self.bitboards[self.turn][piece] ^= move_mask
                    break

            capture_mask = 0b1 << to_square
            for piece, bitboard in enumerate(self.bitboards[~self.turn]):
                if capture_mask & bitboard:
                    self.bitboards[~self.turn][piece] ^= capture_mask
                    break

        # EN-PASSANT CAPTURE
        elif code == 5:
            move_mask = (0b1 << to_square) + (0b1 << from_square)
            for piece, bitboard in enumerate(self.bitboards[self.turn]):
                if move_mask & bitboard:
                    self.bitboards[self.turn][piece] ^= move_mask
                    break

            if self.turn == WHITE:
                capture_mask = self.en_passant >> 8
            else:
                capture_mask = self.en_passant << 8

            self.bitboards[~self.turn][PAWN] ^= capture_mask

        if code != 1:
            self.en_passant = 0

        self.turn = not self.turn
        self.update_pieces()
        self.move_list = self.legal_moves(self.turn)

    def update_pieces(self):

        self.pieces = [self.get_piece_bitboard(WHITE),
                       self.get_piece_bitboard(BLACK)]

        self.all_pieces = self.pieces[WHITE] | self.pieces[BLACK]
        self.empty = ~self.all_pieces

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
        moves += self.legal_pawn_attack_moves(colour)
        return moves

    def legal_single_push_moves(self, colour: int):
        moves = []
        push_targets = single_push_targets(self.bitboards[colour][PAWN],
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
        single_pawn_targets = single_push_targets(self.bitboards[colour][PAWN],
                                                  self.empty, colour)
        double_push_targets = single_push_targets(single_pawn_targets,
                                                  self.empty, colour)

        if colour:
            double_push_targets &= RANK_5_BB
        else:
            double_push_targets &= RANK_4_BB

        indices = get_indices(double_push_targets)

        for to_square in indices:
            if colour:
                from_square = to_square + 16
            else:
                from_square = to_square - 16

            moves.append((1, to_square, from_square))
        return moves

    def legal_pawn_attack_moves(self, colour: int):
        moves = []
        west_attacks = pawn_west_attacks(self.bitboards[colour][PAWN],
                                         self.pieces[~colour], colour)
        east_attacks = pawn_east_attacks(self.bitboards[colour][PAWN],
                                         self.pieces[~colour], colour)
        west_en_passant = pawn_west_attacks(self.bitboards[colour][PAWN],
                                            self.en_passant, colour)
        east_en_passant = pawn_east_attacks(self.bitboards[colour][PAWN],
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
            to_square = move[TO]
            from_square = move[FROM]
            if to_square >= 56 or to_square <= 7:
                for code in range(12, 16):
                    moves.append((code, to_square, from_square))
            else:
                moves.append(move)

        return moves


