import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsTextItem, \
    QGraphicsRectItem, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QBrush

from chessboard import ChessBoard
from bitboard import get_indices
from constants import *


def handle_click_event(index: int):
    global active_square, window
    clicked = 0b1 << index

    if active_square is not None:
        moves = get_valid_moves(active_square)
        for move in moves:
            code, to_square, from_square = move
            if to_square == index and from_square == active_square:
                # TODO Ask about different types of promotion
                chessboard.make_move(move)
                window.chessboard_view.update_chessboard()
                break

        active_square = None
        remove_highlights()
        return
    else:
        if clicked & chessboard.pieces_list[chessboard.turn]:
            active_square = index
            moves = get_valid_moves(active_square)
            highlight_moves(moves)


def get_valid_moves(from_square):
    return [move for move in chessboard.move_list if move[FROM] == from_square]


def remove_highlights():
    global squares
    for index in range(64):
        if is_light_square(index):
            squares[index].setBrush(QBrush(LIGHT_COLOUR))
        else:
            squares[index].setBrush(QBrush(DARK_COLOUR))


def highlight_moves(moves):
    global squares, active_square

    for move in moves + [(-1, active_square, active_square)]:
        index = move[TO]
        if is_light_square(index):
            square_colour = HIGHLIGHTED_LIGHT_COLOUR
        else:
            square_colour = HIGHLIGHTED_DARK_COLOUR

        squares[index].setBrush(QBrush(square_colour))


def is_light_square(index):
    return bool(sum(divmod(index, 8)) % 2)


class ClickableRectItem(QGraphicsRectItem):
    def __init__(self, x, y, size, index, parent=None):
        super().__init__(x, y, size, size, parent)
        self.setAcceptHoverEvents(True)
        self.size = size
        self.index = index

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        handle_click_event(self.index)


class ChessboardWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.chessboard = chessboard
        self.cell_size = self.calculate_cell_size()

        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.update_chessboard()

    def calculate_cell_size(self):
        return min(self.width() // 8, self.height() // 8)

    def update_chessboard(self):
        self.cell_size = self.calculate_cell_size()

        scene = self.scene()
        scene.clear()
        self.draw_squares(scene)
        self.draw_pieces(scene)

    def draw_squares(self, scene):
        global squares
        squares = {}
        for row in range(8):
            for col in range(8):
                x = col * self.cell_size
                y = row * self.cell_size
                index = (7 - col) + (7 - row)*8

                rect = ClickableRectItem(x, y, self.cell_size, index)
                if is_light_square(index):
                    square_colour = LIGHT_COLOUR
                else:
                    square_colour = DARK_COLOUR

                rect.setBrush(QBrush(square_colour))
                scene.addItem(rect)
                squares[index] = rect

        scene.setSceneRect(0, 0, 8 * self.cell_size, 8 * self.cell_size)

    def draw_pieces(self, scene):
        w_pawns_indices = get_indices(self.chessboard.pawns_list[0])
        w_knights_indices = get_indices(self.chessboard.knights_list[0])
        w_bishops_indices = get_indices(self.chessboard.bishops_list[0])
        w_rooks_indices = get_indices(self.chessboard.rooks_list[0])
        w_queens_indices = get_indices(self.chessboard.queens_list[0])
        w_king_indices = get_indices(self.chessboard.king_list[0])

        b_pawns_indices = get_indices(self.chessboard.pawns_list[1])
        b_knights_indices = get_indices(self.chessboard.knights_list[1])
        b_bishops_indices = get_indices(self.chessboard.bishops_list[1])
        b_rooks_indices = get_indices(self.chessboard.rooks_list[1])
        b_queens_indices = get_indices(self.chessboard.queens_list[1])
        b_king_indices = get_indices(self.chessboard.king_list[1])

        self.draw_piece(scene, w_pawns_indices, W_PAWN_ICON)
        self.draw_piece(scene, w_knights_indices, W_KNIGHT_ICON)
        self.draw_piece(scene, w_bishops_indices, W_BISHOP_ICON)
        self.draw_piece(scene, w_rooks_indices, W_ROOK_ICON)
        self.draw_piece(scene, w_queens_indices, W_QUEEN_ICON)
        self.draw_piece(scene, w_king_indices, W_KING_ICON)

        self.draw_piece(scene, b_pawns_indices, B_PAWN_ICON)
        self.draw_piece(scene, b_knights_indices, B_KNIGHT_ICON)
        self.draw_piece(scene, b_bishops_indices, B_BISHOP_ICON)
        self.draw_piece(scene, b_rooks_indices, B_ROOK_ICON)
        self.draw_piece(scene, b_queens_indices, B_QUEEN_ICON)
        self.draw_piece(scene, b_king_indices, B_KING_ICON)

    def draw_piece(self, scene, indices, icon):
        for index in indices:
            row, col = divmod(index, 8)
            x = (7 - col) * self.cell_size
            y = (7 - row) * self.cell_size

            text_item = QGraphicsTextItem(icon)
            font_size = int(self.cell_size * 0.8)  # Increase the font size for larger pieces
            text_item.setFont(QFont("Arial", font_size, weight=QFont.Weight.Bold))
            text_width = text_item.boundingRect().width()
            text_height = text_item.boundingRect().height()
            text_item.setPos(x + (self.cell_size - text_width) / 2, y + (self.cell_size - text_height) / 2)
            text_item.setDefaultTextColor(QColor(0, 0, 0))  # Set text colour to black
            scene.addItem(text_item)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_chessboard()


class ChessboardGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chessboard GUI")
        self.setGeometry(100, 100, 600, 600)  # Set the default window size to 600x600

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.chessboard_view = ChessboardWidget()
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().addWidget(self.chessboard_view)

        self.show()


def main():
    global chessboard, active_square, squares, window
    active_square = None
    chessboard = ChessBoard()

    app = QApplication(sys.argv)
    window = ChessboardGUI()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
