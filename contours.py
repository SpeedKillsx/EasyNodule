import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import cv2
import numpy as np

class MainWindow(QMainWindow):   
    def __init__(self, image):
        super().__init__()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ressources/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # Créer une instance de la figure Matplotlib
        self.figure = Figure()

        # Créer un canevas Matplotlib
        self.canvas = FigureCanvas(self.figure)

        # Créer une barre d'outils pour Matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Créer un widget central et un layout vertical
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Définir le widget central
        self.setCentralWidget(central_widget)

        # Charger l'image passée en argument
        self.image = image

        # Détecter les contours de l'image
        contours = self.detecter_contours(self.image)

        # Afficher l'image avec les contours
        self.afficher_image_contours(self.image, contours)  
    def detecter_contours(self, image):
       

        # Appliquer un flou gaussien pour réduire le bruit
        blurred = cv2.GaussianBlur(image, (3, 3), 0)

        # Détecter les contours avec l'algorithme de Canny
        edges = cv2.Canny(blurred, 90, 200)
        kernel = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        # Trouver les contours dans l'image
        contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        MIN_NODULE_AREA = 45
        filtered_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > MIN_NODULE_AREA:
                filtered_contours.append(contour)
        return filtered_contours

    def afficher_image_contours(self, image, contours):
        # Créer une nouvelle figure Matplotlib
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Dessiner les contours sur l'image
        ax.imshow(image, cmap="gray")
        ax.axis('off')

        # Dessiner les contours sur la figure
        for contour in contours:
            ax.plot(contour[:, 0, 0], contour[:, 0, 1], 'r', linewidth=2)

        # Mettre à jour le canevas
        self.canvas.draw()

if __name__ == '__main__':
    # Vérifier si une image a été passée en argument
    if len(sys.argv) < 2:
        print("Veuillez spécifier le chemin de l'image en argument.")
        sys.exit(1)

    # Charger l'image depuis le chemin spécifié
    image_path = sys.argv[1]
    image = np.load(image_path, allow_pickle=True)

    # Créer l'application PyQt5
    app = QApplication(sys.argv)

    # Créer la fenêtre principale en passant l'image en argument
    window = MainWindow(image[32,:,:])
    #window.setStyleSheet("background-color: rgb(31, 35, 42);")

    # Appliquer un style spécifique à la barre d'outils
    toolbar_style = """
        QToolBar{
        background-color:rgb(31, 35, 42);
        border: black;

        }
        QToolButton:hover {
            background-color: red;
        }
        QToolButton:checked {
            background-color: green;
        }
        QMenu {
            background-color: yellow;
        }
        
       
        
        
    """
    window.toolbar.setStyleSheet(toolbar_style)
     # Modifier le style des fonctionnalités individuelles
    # Modifier le style des fonctionnalités individuelles
    
    window.setWindowTitle('Contours visualisation')

    # Afficher la fenêtre principale
    window.show()

    # Exécuter l'application PyQt5
    sys.exit(app.exec_())