import os
import sys
from PySide2 import *
from ui_interface import *
from Custom_Widgets.Widgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui)
        ########################################################################

        ########################################################################
        
        
        self.show()
        #close center menu 
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())
            
        #expand right menu size
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())


        #close right menu 
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())

        #close Notification 
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())
        
        #expand center menu size
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        
        """self.ui.textIdC.setText("C02555")
        self.ui.textUsernameC.setText("user_124")
        self.ui.textNameC.setText("KOULAL")
        self.ui.textHospital.setText("AlgerH")
        self.ui.textWilayaC.setText("Tizi Ouzou")
        self.ui.textGrade.setText("Pr")
        """
        #Open file btn
        self.ui.openfileBtn.clicked.connect(self.clicker)
        
        #matplolib
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout(self.ui.frame_matplotlib)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        #canva
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #end of canva
        
        #add canva
        self.horizontalLayout_44.addWidget(self.canvas)
        
    def clicker(self):
        print("You clicked the button to choose a file !")
        fname = QFileDialog.getOpenFileName(self, "Open File and Choose the 3D Nodule", "" , "All Files (*);; Python Files(*.npy)")
        Nodule3D = np.load(fname[0], allow_pickle=True)
        #print(Nodule3D.shape)   
        #plt.plot(Nodule3D[10,:,:,0])
        #plt.show()
        
        #Clear the canvas 
        self.figure.clear()
        #plot
        im = Image.fromarray(Nodule3D[0,0][32,:,:])
        #im.show()
        plt.imshow(Nodule3D[0,0][32,:,:],'gray')
        #refresh
        self.canvas.draw()
        
    
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        