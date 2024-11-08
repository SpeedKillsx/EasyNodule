import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Créer un widget central et le définir comme le widget principal de la fenêtre
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Créer un layout en grille
        layout = QGridLayout(central_widget)

        # Créer les figures pour les images
        self.figure_top = plt.figure()
        self.figure_bottom1 = plt.figure()
        self.figure_bottom2 = plt.figure()
        self.figure_bottom3 = plt.figure()

        self.figure_bottom4 = plt.figure()
        self.figure_bottom5 = plt.figure()
        self.figure_bottom6 = plt.figure()

        # Créer les canvas pour les figures
        self.canvas_top = FigureCanvas(self.figure_top)
        self.canvas_bottom1 = FigureCanvas(self.figure_bottom1)
        self.canvas_bottom2 = FigureCanvas(self.figure_bottom2)
        self.canvas_bottom3 = FigureCanvas(self.figure_bottom3)
        
        self.canvas_bottom4 = FigureCanvas(self.figure_bottom4)
        self.canvas_bottom5 = FigureCanvas(self.figure_bottom5)
        self.canvas_bottom6 = FigureCanvas(self.figure_bottom6)

        # Ajouter les canvas des images au layout en utilisant les positions de grille
        layout.addWidget(self.canvas_top, 0, 0, 1, 3)
        
        layout.addWidget(self.canvas_bottom1, 1, 0)
        layout.addWidget(self.canvas_bottom2, 1, 1)
        layout.addWidget(self.canvas_bottom3, 1, 2)
        
        layout.addWidget(self.canvas_bottom4, 2, 0)
        layout.addWidget(self.canvas_bottom5, 2, 1)
        layout.addWidget(self.canvas_bottom6, 2, 2)
        
        tool = NavigationToolbar(self.canvas_top, central_widget)
        layout.addWidget(tool)
        # Charger les images
        self.load_images()
        

    def load_images(self):
        # Charger les images à afficher (remplacez les chemins d'accès par vos propres images)
        datas = np.load("XTrain_X_aug.npy")
        image_path_top = datas[0]
        image_path_bottom1 = datas[1]
        image_path_bottom2 = "ressources/bg.jpg"
        image_path_bottom3 = "ressources/bg.jpg"

        # Afficher les images en utilisant Matplotlib
        self.figure_top.clear()
        self.ax_top = self.figure_top.add_subplot(111)
        self.ax_top.imshow(image_path_top)
        self.ax_top.set_title("org")
        self.canvas_top.draw()

        self.figure_bottom1.clear()
        self.ax_bottom1 = self.figure_bottom1.add_subplot(111)
        self.ax_bottom1.imshow(image_path_bottom1)
        self.ax_bottom1.set_title("X")
        self.canvas_bottom1.draw()

        self.figure_bottom2.clear()
        self.ax_bottom2 = self.figure_bottom2.add_subplot(111)
        self.ax_bottom2.imshow(plt.imread(image_path_bottom2))
        self.canvas_bottom2.draw()

        self.figure_bottom3.clear()
        self.ax_bottom3 = self.figure_bottom3.add_subplot(111)
        self.ax_bottom3.imshow(plt.imread(image_path_bottom3))
        self.canvas_bottom3.draw()
        
        

if __name__ == "__main__":
    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    # Exécuter la boucle principale de l'application
    sys.exit(app.exec_())
