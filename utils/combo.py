import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste des Wilayas Algériennes")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        label = QLabel("Sélectionnez une wilaya :")
        self.combo_box = QComboBox()

        # Ajouter les noms des wilayas algériennes au ComboBox
        wilayas = [
            "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa",
            "Biskra", "Béchar", "Blida", "Bouira", "Tamanrasset", "Tébessa",
            "Tlemcen", "Tiaret", "Tizi Ouzou", "Alger", "Djelfa", "Jijel",
            "Sétif", "Saïda", "Skikda", "Sidi Bel Abbès", "Annaba", "Guelma",
            "Constantine", "Médéa", "Mostaganem", "M'Sila", "Mascara",
            "Ouargla", "Oran", "El Bayadh", "Illizi", "Bordj Bou Arreridj",
            "Boumerdès", "El Tarf", "Tindouf", "Tissemsilt", "El Oued",
            "Khenchela", "Souk Ahras", "Tipaza", "Mila", "Aïn Defla",
            "Naâma", "Aïn Témouchent", "Ghardaïa", "Relizane"
        ]

        self.combo_box.addItems(wilayas)

        layout.addWidget(label)
        layout.addWidget(self.combo_box)
        self.setLayout(layout)

        self.combo_box.currentIndexChanged.connect(self.selection_changed)

    def selection_changed(self, index):
        selected_wilaya = self.combo_box.itemText(index)
        print("Wilaya sélectionnée :", selected_wilaya)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
