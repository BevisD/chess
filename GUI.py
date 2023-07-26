import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsTextItem, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QBrush


class ChessboardWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

        scene = QGraphicsScene(self)
        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.updateChessboard()

    def updateChessboard(self):
        scene = self.scene()
        scene.clear()

        cell_size = min(self.width() // 8, self.height() // 8)

        # Dictionary representing the initial chessboard state
        starting_positions = {
            (0, 0): '♜', (0, 1): '♞', (0, 2): '♝', (0, 3): '♛', (0, 4): '♚', (0, 5): '♝', (0, 6): '♞', (0, 7): '♜',
            (1, 0): '♟', (1, 1): '♟', (1, 2): '♟', (1, 3): '♟', (1, 4): '♟', (1, 5): '♟', (1, 6): '♟', (1, 7): '♟',
            (6, 0): '♙', (6, 1): '♙', (6, 2): '♙', (6, 3): '♙', (6, 4): '♙', (6, 5): '♙', (6, 6): '♙', (6, 7): '♙',
            (7, 0): '♖', (7, 1): '♘', (7, 2): '♗', (7, 3): '♕', (7, 4): '♔', (7, 5): '♗', (7, 6): '♘', (7, 7): '♖'
        }

        for row in range(8):
            for col in range(8):
                x = col * cell_size
                y = row * cell_size
                rect = QRectF(x, y, cell_size, cell_size)
                square_color = QColor(240, 217, 181) if (row + col) % 2 == 0 else QColor(181, 136, 99)
                scene.addRect(rect, brush=QBrush(square_color))

                # Draw the chess pieces on their initial squares using Unicode characters
                piece = starting_positions.get((row, col))
                if piece:
                    text_item = QGraphicsTextItem(piece)
                    font_size = int(cell_size * 0.8)  # Increase the font size for larger pieces
                    text_item.setFont(QFont("Arial", font_size, weight=QFont.Weight.Bold))  # Set bold font for better visibility
                    text_width = text_item.boundingRect().width()
                    text_height = text_item.boundingRect().height()
                    text_item.setPos(x + (cell_size - text_width) / 2, y + (cell_size - text_height) / 2)
                    text_item.setDefaultTextColor(QColor(0, 0, 0))  # Set text color to black
                    scene.addItem(text_item)

        scene.setSceneRect(0, 0, 8 * cell_size, 8 * cell_size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateChessboard()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChessboardGUI()
    sys.exit(app.exec())
