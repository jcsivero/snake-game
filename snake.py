import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtGui import QPainter, QColor, QBrush, QFont
from PySide6.QtCore import Qt, QTimer, QRect

# --- Configuración ---
ANCHO = 600
ALTO = 600
TAMANO_CELDA = 20
COLUMNAS = ANCHO // TAMANO_CELDA
FILAS = ALTO // TAMANO_CELDA
VELOCIDAD = 120  # ms entre cada fotograma

COLOR_FONDO = QColor("#1a1a2e")
COLOR_SERPIENTE = QColor("#00ff88")
COLOR_COMIDA = QColor("#ff4757")
COLOR_TEXTO = QColor("#ffffff")
COLOR_CABEZA = QColor("#00cc66")
COLOR_GRID = QColor("#16213e")
COLOR_GAMEOVER_TEXT = QColor("#ff4757")
COLOR_GAMEOVER_FADE = QColor(45, 45, 78, 150)


class GameBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.reiniciar()

    def reiniciar(self):
        self.serpiente = [(COLUMNAS // 2, FILAS // 2)]
        self.direccion = (1, 0)
        self.siguiente_direccion = (1, 0)
        self.comida = self.nueva_comida()
        self.puntuacion = 0
        self.en_juego = True
        if not hasattr(self, 'timer'):
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.actualizar)
        self.timer.start(VELOCIDAD)
        self.update()

    def nueva_comida(self):
        while True:
            pos = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
            if pos not in self.serpiente:
                return pos

    def actualizar(self):
        if not self.en_juego:
            self.timer.stop()
            self.update()
            return

        self.direccion = self.siguiente_direccion
        dx, dy = self.direccion
        cx, cy = self.serpiente[0]
        nueva_cabeza = (cx + dx, cy + dy)

        if not (0 <= nueva_cabeza[0] < COLUMNAS and 0 <= nueva_cabeza[1] < FILAS):
            self.fin_del_juego()
            return
        if nueva_cabeza in self.serpiente:
            self.fin_del_juego()
            return

        self.serpiente.insert(0, nueva_cabeza)

        if nueva_cabeza == self.comida:
            self.puntuacion += 10
            self.comida = self.nueva_comida()
        else:
            self.serpiente.pop()

        self.update()

    def fin_del_juego(self):
        self.en_juego = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fondo
        painter.fillRect(self.rect(), COLOR_FONDO)

        if self.en_juego:
            self.dibujar_juego(painter)
        else:
            self.dibujar_fin_del_juego(painter)

    def dibujar_juego(self, painter):
        # Grid
        for i in range(0, ANCHO, TAMANO_CELDA):
            painter.setPen(COLOR_GRID)
            painter.drawLine(i, 0, i, ALTO)
        for j in range(0, ALTO, TAMANO_CELDA):
            painter.setPen(COLOR_GRID)
            painter.drawLine(0, j, ANCHO, j)

        # Comida
        fx, fy = self.comida
        painter.setBrush(COLOR_COMIDA)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRect(fx * TAMANO_CELDA + 3, fy * TAMANO_CELDA + 3, TAMANO_CELDA - 6, TAMANO_CELDA - 6))

        # Serpiente
        for i, (x, y) in enumerate(self.serpiente):
            color = COLOR_CABEZA if i == 0 else COLOR_SERPIENTE
            painter.setBrush(color)
            painter.drawRect(x * TAMANO_CELDA + 1, y * TAMANO_CELDA + 1, TAMANO_CELDA - 2, TAMANO_CELDA - 2)

        # Puntuación
        painter.setPen(COLOR_TEXTO)
        painter.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        painter.drawText(10, 20, f"Puntuación: {self.puntuacion}")

    def dibujar_fin_del_juego(self, painter):
         # Dibujar serpiente difuminada
        for x, y in self.serpiente:
            painter.setBrush(QColor("#2d2d4e"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(x * TAMANO_CELDA + 1, y * TAMANO_CELDA + 1, TAMANO_CELDA - 2, TAMANO_CELDA - 2)

        painter.fillRect(self.rect(), COLOR_GAMEOVER_FADE)
        
        cx, cy = ANCHO // 2, ALTO // 2
        painter.setPen(COLOR_GAMEOVER_TEXT)
        painter.setFont(QFont("Consolas", 36, QFont.Weight.Bold))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "GAME OVER")
        
        painter.setPen(COLOR_TEXTO)
        painter.setFont(QFont("Consolas", 20))
        painter.drawText(0, cy + 40, ANCHO, 30, Qt.AlignmentFlag.AlignCenter, f"Puntuación: {self.puntuacion}")

        painter.setPen(QColor("#aaaaaa"))
        painter.setFont(QFont("Consolas", 14))
        painter.drawText(0, cy + 80, ANCHO, 30, Qt.AlignmentFlag.AlignCenter, "Pulsa R para reiniciar")


    def keyPressEvent(self, event):
        tecla = event.key()
        opuestos = {(1, 0): (-1, 0), (-1, 0): (1, 0), (0, 1): (0, -1), (0, -1): (0, 1)}

        nueva_dir = None
        if tecla in (Qt.Key.Key_Up, Qt.Key.Key_W):
            nueva_dir = (0, -1)
        elif tecla in (Qt.Key.Key_Down, Qt.Key.Key_S):
            nueva_dir = (0, 1)
        elif tecla in (Qt.Key.Key_Left, Qt.Key.Key_A):
            nueva_dir = (-1, 0)
        elif tecla in (Qt.Key.Key_Right, Qt.Key.Key_D):
            nueva_dir = (1, 0)
        elif tecla == Qt.Key.Key_R:
            self.reiniciar()
        
        if nueva_dir and nueva_dir != opuestos.get(self.direccion):
            self.siguiente_direccion = nueva_dir


class SnakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake")
        self.board = GameBoard(self)
        self.setCentralWidget(self.board)
        self.setFixedSize(ANCHO, ALTO)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeWindow()
    window.show()
    sys.exit(app.exec())
