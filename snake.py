import tkinter as tk
import random

# --- Configuración ---
ANCHO = 600
ALTO = 600
TAMANO_CELDA = 20
COLUMNAS = ANCHO // TAMANO_CELDA
FILAS = ALTO // TAMANO_CELDA
VELOCIDAD = 120  # ms entre cada fotograma

COLOR_FONDO = "#1a1a2e"
COLOR_SERPIENTE = "#00ff88"
COLOR_CABEZA = "#00cc66"
COLOR_COMIDA = "#ff4757"
COLOR_TEXTO = "#ffffff"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas.pack()

        self.root.bind("<KeyPress>", self.cambiar_direccion)
        self.root.bind("<r>", lambda e: self.reiniciar())
        self.root.bind("<R>", lambda e: self.reiniciar())

        self.reiniciar()

    def reiniciar(self):
        self.serpiente = [(COLUMNAS // 2, FILAS // 2)]
        self.direccion = (1, 0)
        self.siguiente_direccion = (1, 0)
        self.comida = self.nueva_comida()
        self.puntuacion = 0
        self.en_juego = True
        self.actualizar()

    def nueva_comida(self):
        while True:
            pos = (random.randint(0, COLUMNAS - 1), random.randint(0, FILAS - 1))
            if pos not in self.serpiente:
                return pos

    def cambiar_direccion(self, event):
        tecla = event.keysym
        opuestos = {(1, 0): (-1, 0), (-1, 0): (1, 0), (0, 1): (0, -1), (0, -1): (0, 1)}
        mapa = {
            "Up": (0, -1), "w": (0, -1), "W": (0, -1),
            "Down": (0, 1), "s": (0, 1), "S": (0, 1),
            "Left": (-1, 0), "a": (-1, 0), "A": (-1, 0),
            "Right": (1, 0), "d": (1, 0), "D": (1, 0),
        }
        if tecla in mapa:
            nueva = mapa[tecla]
            if nueva != opuestos.get(self.direccion):
                self.siguiente_direccion = nueva

    def actualizar(self):
        if not self.en_juego:
            return

        self.direccion = self.siguiente_direccion
        dx, dy = self.direccion
        cx, cy = self.serpiente[0]
        nueva_cabeza = (cx + dx, cy + dy)

        # Colisión con paredes
        if not (0 <= nueva_cabeza[0] < COLUMNAS and 0 <= nueva_cabeza[1] < FILAS):
            self.fin_del_juego()
            return

        # Colisión consigo misma
        if nueva_cabeza in self.serpiente:
            self.fin_del_juego()
            return

        self.serpiente.insert(0, nueva_cabeza)

        if nueva_cabeza == self.comida:
            self.puntuacion += 10
            self.comida = self.nueva_comida()
        else:
            self.serpiente.pop()

        self.dibujar()
        self.root.after(VELOCIDAD, self.actualizar)

    def dibujar(self):
        self.canvas.delete("all")

        # Grid sutil
        for i in range(0, ANCHO, TAMANO_CELDA):
            self.canvas.create_line(i, 0, i, ALTO, fill="#16213e", width=1)
        for j in range(0, ALTO, TAMANO_CELDA):
            self.canvas.create_line(0, j, ANCHO, j, fill="#16213e", width=1)

        # Comida
        fx, fy = self.comida
        self.canvas.create_oval(
            fx * TAMANO_CELDA + 3, fy * TAMANO_CELDA + 3,
            fx * TAMANO_CELDA + TAMANO_CELDA - 3, fy * TAMANO_CELDA + TAMANO_CELDA - 3,
            fill=COLOR_COMIDA, outline=""
        )

        # Serpiente
        for i, (x, y) in enumerate(self.serpiente):
            color = COLOR_CABEZA if i == 0 else COLOR_SERPIENTE
            self.canvas.create_rectangle(
                x * TAMANO_CELDA + 1, y * TAMANO_CELDA + 1,
                x * TAMANO_CELDA + TAMANO_CELDA - 1, y * TAMANO_CELDA + TAMANO_CELDA - 1,
                fill=color, outline=""
            )

        # Puntuación
        self.canvas.create_text(10, 10, anchor="nw", text=f"Puntuación: {self.puntuacion}",
                                fill=COLOR_TEXTO, font=("Consolas", 14, "bold"))

    def fin_del_juego(self):
        self.en_juego = False
        self.canvas.delete("all")

        # Fondo oscurecido
        self.canvas.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_FONDO, outline="")

        # Dibujar serpiente difuminada
        for x, y in self.serpiente:
            self.canvas.create_rectangle(
                x * TAMANO_CELDA + 1, y * TAMANO_CELDA + 1,
                x * TAMANO_CELDA + TAMANO_CELDA - 1, y * TAMANO_CELDA + TAMANO_CELDA - 1,
                fill="#2d2d4e", outline=""
            )

        cx, cy = ANCHO // 2, ALTO // 2
        self.canvas.create_text(cx, cy - 60, text="GAME OVER", fill=COLOR_COMIDA,
                                font=("Consolas", 36, "bold"))
        self.canvas.create_text(cx, cy, text=f"Puntuación: {self.puntuacion}", fill=COLOR_TEXTO,
                                font=("Consolas", 20))
        self.canvas.create_text(cx, cy + 50, text="Pulsa R para reiniciar", fill="#aaaaaa",
                                font=("Consolas", 14))


if __name__ == "__main__":
    root = tk.Tk()
    juego = SnakeGame(root)
    root.mainloop()
