import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import sqlite3
import matplotlib.pyplot as plt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistiques de la base de données")

        # Créer un widget QWidget avec un layout QVBoxLayout
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Se connecter à la base de données
        self.conn = sqlite3.connect("NoduleDataBase.db")
        self.cursor = self.conn.cursor()

        # Obtenir les statistiques à partir de la base de données
        stats = self.get_statistics()
        print("les stats = ", stats)
        # Créer un graphique camembert
        self.fig, self.ax = plt.subplots()
        wedges, labels, autotexts = self.ax.pie(stats.values(), autopct="%1.1f%%", startangle=90)
        self.ax.axis("equal")

        # Ajouter les légendes
        self.ax.legend(wedges, stats.keys(), title="Wilaya", loc="center left", bbox_to_anchor=(0.87, 0.5))
        self.ax.set_title("Statistiques des nodules malins par wilaya")

        # Ajouter le graphique au layout
        self.layout.addWidget(self.fig.canvas)

    def get_statistics(self):
        # Exécutez les requêtes sur la base de données pour obtenir les statistiques
        self.cursor.execute("SELECT WilayaP, COUNT(*) FROM Patient WHERE idP in (SELECT idP from Nodule where NoduleClassification == '1') GROUP BY WilayaP")
        results = self.cursor.fetchall()
        print(results)
        # Générer les statistiques sous forme de dictionnaire
        stats = {result[0]: result[1] for result in results}

        return stats

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Ajuster la disposition des éléments du graphique
    window.fig.tight_layout()

    sys.exit(app.exec_())
