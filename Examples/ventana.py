from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import numpy as np

# Función para renderizar una ecuación LaTeX y convertirla en una imagen de QPixmap
def render_latex(formula, fontsize=12):
    fig = plt.figure()
    text = fig.text(0, 0, f"${formula}$", fontsize=fontsize)
    fig.canvas.draw()

    bbox = text.get_window_extent()
    width, height = int(bbox.width), int(bbox.height)

    fig.set_size_inches(width / fig.dpi, height / fig.dpi)
    fig.canvas.draw()
    
    # Obtener la imagen de la figura en formato RGBA
    image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    image = image.reshape((height, width, 4))
    plt.close(fig)

    # Convertir la imagen de numpy a QImage
    qimage = QImage(image.data, width, height, QImage.Format.Format_RGBA8888)
    return QPixmap.fromImage(qimage)

app = QApplication([])

# Crear una ventana principal
window = QWidget()
layout = QVBoxLayout()

# Etiqueta para la ecuación LaTeX
label = QLabel()
pixmap = render_latex(r"\frac{a}{b} + \sqrt{c} = d")
label.setPixmap(pixmap)

# Agregar el QLabel al diseño de la ventana
layout.addWidget(label)
window.setLayout(layout)

# Mostrar la ventana
window.show()
app.exec()

