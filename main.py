import os
import sys
from PySide2 import *
from interface_ui import *
from Custom_Widgets.Widgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import numpy as np
from PIL import Image
from Preporcessing import *
from Database_methods import *
class MainWindow(QMainWindow):
    def LoadModels(self):
        path_modelX = "Models/ModelX/capsule-5"
        path_modelY = "Models/Model_y_92/capsule-5"
        path_modelZ = "Models/ModelZ/capsule-5"
        #! loadX
        self.ModelX = CapsuleNetwork(**params)
        Xcheckpoint = tf.train.Checkpoint(model=self.ModelX)
        Xcheckpoint.restore(path_modelX)
        #! loadY
        self.ModelY = CapsuleNetwork(**params)
        Ycheckpoint = tf.train.Checkpoint(model=self.ModelY)
        Ycheckpoint.restore(path_modelY)
        #! loadZ
        self.ModelZ = CapsuleNetwork(**params)
        Zcheckpoint = tf.train.Checkpoint(model=self.ModelZ)
        Zcheckpoint.restore(path_modelZ)
        
    def StartClassification(self):
        if self.PatientID is not None and self.PSelected == True and self.scan !="":
            #! Load all models
            self.LoadModels()
            #! Make a prediction
            classification = final_predMAJOR(self.Nodule3D[:,:,32], self.Nodule3D[:,32,:],self.Nodule3D[32,:,:],self.ModelX,self.ModelY,self.ModelZ)
            result = None
            if classification == 0:
                result="benin"
            else:
                result="malignant"
            print(result)
            
            ##! X Classification
            prX, valX = predict_proba(self.ModelX,tf.expand_dims(Preprocessing(self.Nodule3D[:,:,32]),0))
            print(valX[0])
            self.ui.label_X_2.setText(str(np.max(prX)*100))
            ##! Y Classification
            prY, valY = predict_proba(self.ModelY,tf.expand_dims(Preprocessing(self.Nodule3D[:,32,:]),0))
            self.ui.label_Y_4.setText(str(np.max(prY)*100))
            ##! Z Classification
            prZ, valZ = predict_proba(self.ModelZ,tf.expand_dims(Preprocessing(self.Nodule3D[32,:,:]),0))
            self.ui.label_Z_5.setText(str(np.max(prZ)*100))
            self.ui.label_12.setText("Final Classification: "+result)
            self.PatientID = None
            self.PSelected = False
        else:
            self.msg.setText("You must choose a patient befor starting the classification")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            
    def ShowLabels(self):
        #* Display labels on window
        self.ui.label_addPName.show()
        self.ui.label_addPWilaya.show()
        self.ui.label_addPWilaya_2.show()
        self.ui.label_addPSexe.show()
        self.ui.label_addPAllergies.show()
        self.ui.label_addPSmoking.show()
        self.ui.label_addPMedHist.show()
        self.ui.label_addPEmail.show()
        self.ui.label_addPNumber.show()
        #* Display textEdits on window
        self.ui.textNamePADD.show()
        self.ui.textWilayaPADD.show()
        self.ui.dateEditPADD.show()
        self.ui.textSexePADD.show()
        self.ui.textAllergiesPADD.show()
        self.ui.textSmokingPADD.show()
        self.ui.textMedHistPADD.show()
        self.ui.textEmailPADD.show()
        self.ui.textNumberPADD.show()
        self.ui.addPateintBtn.show()
        self.ui.tableWidget.hide()
    def hideLabels(self):
        #* Hide labels and TextEdits
        self.ui.label_addPName.hide()
        self.ui.label_addPWilaya.hide()
        self.ui.label_addPWilaya_2.hide()
        self.ui.label_addPSexe.hide()
        self.ui.label_addPAllergies.hide()
        self.ui.label_addPSmoking.hide()
        self.ui.label_addPMedHist.hide()
        self.ui.label_addPEmail.hide()
        self.ui.label_addPNumber.hide()
        
        self.ui.textNamePADD.hide()
        self.ui.textWilayaPADD.hide()
        self.ui.dateEditPADD.hide()
        self.ui.textSexePADD.hide()
        self.ui.textAllergiesPADD.hide()
        self.ui.textSmokingPADD.hide()
        self.ui.textMedHistPADD.hide()
        self.ui.textEmailPADD.hide()
        self.ui.textNumberPADD.hide()
        self.ui.addPateintBtn.hide()
    def ResearchPatient(self):
        self.hideLabels()
        #? Check if the patient exist in the database
        if PatientResearchPhoneName(self.ui.textPhaneNumberSearch.toPlainText(), self.ui.textNamePatientSearch.toPlainText()) ==1:
            #* show the patient info in the table 
            self.add_data()
        else:
            #! The patient doesn't exist, we display labels if the labels are filled , or we display all the database
            self.msg.setText("There is no patient with this name and phone number")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            #! Here the patient will be added
            if self.ui.textPhaneNumberSearch.toPlainText()!="" and self.ui.textNamePatientSearch.toPlainText()!="":
                self.ShowLabels()
            else:
                self.add_data()
            
    #? Add a patient
    def AddPatient(self):
        if PatientResearchPhoneName(PhonePatient=self.ui.textNumberPADD.toPlainText(), NamePatient=self.ui.textNamePADD.toPlainText())==-1:
            self.ShowLabels()
            if(self.ui.textNamePADD.toPlainText()!="" and self.ui.textWilayaPADD.toPlainText()!="" and self.ui.dateEditPADD.text()!="" and self.ui.textSexePADD.toPlainText()!="" and self.ui.textAllergiesPADD.toPlainText()!="" and self.ui.textSmokingPADD.toPlainText() !="" and self.ui.textMedHistPADD.toPlainText()!=""and self.ui.textEmailPADD.toPlainText()!="" and self.ui.textNumberPADD.toPlainText() !=""):
                    if len(self.ui.textNumberPADD.toPlainText()) == 10:
                        value_familly = 0
                        PatientInsert(self.ui.textNamePADD.toPlainText(),
                                    self.ui.dateEditPADD.text(),
                                    self.ui.textWilayaPADD.toPlainText(),
                                    self.ui.textSexePADD.toPlainText(),
                                    self.ui.textAllergiesPADD.toPlainText(),
                                    self.ui.textSmokingPADD.toPlainText(),
                                    self.ui.textMedHistPADD.toPlainText(),
                                    str(value_familly),
                                    self.ui.textEmailPADD.toPlainText(),
                                    self.ui.textNumberPADD.toPlainText()
                                    )
                        self.ui.addPateintBtn.hide()
                        self.ui.label_addPName.hide()
                        self.ui.label_addPWilaya.hide()
                        self.ui.label_addPWilaya_2.hide()
                        self.ui.label_addPSexe.hide()
                        self.ui.label_addPAllergies.hide()
                        self.ui.label_addPSmoking.hide()
                        self.ui.label_addPMedHist.hide()
                        self.ui.label_addPEmail.hide()
                        self.ui.label_addPNumber.hide()
                        
                        self.ui.textNamePADD.hide()
                        self.ui.textWilayaPADD.hide()
                        self.ui.dateEditPADD.hide()
                        self.ui.textSexePADD.hide()
                        self.ui.textAllergiesPADD.hide()
                        self.ui.textSmokingPADD.hide()
                        self.ui.textMedHistPADD.hide()
                        self.ui.textEmailPADD.hide()
                        self.ui.textNumberPADD.hide()
                        self.add_data()
                        self.msg.setText("Patient added succefully.")
                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msg.exec_()
                    else:
                        
                        self.msg.setText("Incorrect Number Phone.")
                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msg.exec_()
            else:
                self.msg.setText("Fill all the fileds, please.")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
        else:
            self.msg.setText("The patient already exist.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            
    #? Print data in the table
    def add_data(self):
        """
            Print the data in the table, and contuniously refresh the table after a research
        """
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.show()
        row_count = self.ui.tableWidget.rowCount()
        print(row_count)
        self.ui.tableWidget.insertRow(row_count)
        #! Check if the patient exist in the table patient
        if PatientResearchPhoneName(self.ui.textPhaneNumberSearch.toPlainText(), self.ui.textNamePatientSearch.toPlainText()) == 1:
            #* Get the patient's information if he exists
            data = PatientInfoByPhoneName(self.ui.textPhaneNumberSearch.toPlainText(), self.ui.textNamePatientSearch.toPlainText())
            id_item = QTableWidgetItem(str(data[0]))
            name_item = QTableWidgetItem(str(data[1]))
            birthday_item = QTableWidgetItem(data[2])
            wilaya_item = QTableWidgetItem(str(data[3]))
            sex_item = QTableWidgetItem(str(data[4]))
            allergies_item = QTableWidgetItem(data[5])
            smoking_item = QTableWidgetItem(str(data[6]))
            medhist_item = QTableWidgetItem(str(data[7]))
            cancerf_item = QTableWidgetItem(str(data[8]))
            eamil_item = QTableWidgetItem(str(data[9]))
            phone_item = QTableWidgetItem(str(data[10]))
            
            self.ui.tableWidget.setItem(row_count, 0, id_item)
            self.ui.tableWidget.setItem(row_count, 1, name_item)
            self.ui.tableWidget.setItem(row_count, 2, birthday_item)
            self.ui.tableWidget.setItem(row_count, 3, wilaya_item)
            self.ui.tableWidget.setItem(row_count, 4, sex_item)
            self.ui.tableWidget.setItem(row_count, 5, allergies_item)
            self.ui.tableWidget.setItem(row_count, 6, smoking_item)
            self.ui.tableWidget.setItem(row_count, 7, medhist_item)
            self.ui.tableWidget.setItem(row_count, 8, cancerf_item)
            self.ui.tableWidget.setItem(row_count, 9, eamil_item)
            self.ui.tableWidget.setItem(row_count, 10, phone_item)
        else:
            #* If the patient doesn't exist, we print information of all the patient (the research labels should be blank, at least one of them)
            data = PatientInfoByPhoneName("", "")
            data = list(data)
            print(len(data))
            if row_count == 0:
                for i in range(len(data)):
                    self.ui.tableWidget.insertRow(row_count)
                    id_item = QTableWidgetItem(str(data[i][0]))
                    name_item = QTableWidgetItem(str(data[i][1]))
                    birthday_item = QTableWidgetItem(data[i][2])
                    wilaya_item = QTableWidgetItem(str(data[i][3]))
                    sex_item = QTableWidgetItem(str(data[i][4]))
                    allergies_item = QTableWidgetItem(data[i][5])
                    smoking_item = QTableWidgetItem(str(data[i][6]))
                    medhist_item = QTableWidgetItem(str(data[i][7]))
                    cancerf_item = QTableWidgetItem(str(data[i][8]))
                    eamil_item = QTableWidgetItem(str(data[i][9]))
                    phone_item = QTableWidgetItem(str(data[i][10]))
                    self.ui.tableWidget.setItem(row_count, 0, id_item)
                    self.ui.tableWidget.setItem(row_count, 1, name_item)
                    self.ui.tableWidget.setItem(row_count, 2, birthday_item)
                    self.ui.tableWidget.setItem(row_count, 3, wilaya_item)
                    self.ui.tableWidget.setItem(row_count, 4, sex_item)
                    self.ui.tableWidget.setItem(row_count, 5, allergies_item)
                    self.ui.tableWidget.setItem(row_count, 6, smoking_item)
                    self.ui.tableWidget.setItem(row_count, 7, medhist_item)
                    self.ui.tableWidget.setItem(row_count, 8, cancerf_item)
                    self.ui.tableWidget.setItem(row_count, 9, eamil_item)
                    self.ui.tableWidget.setItem(row_count, 10, phone_item)
                    row_count = row_count + 1
            else:
                id_item = QTableWidgetItem(str(data[-1][0]))
                name_item = QTableWidgetItem(str(data[-1][1]))
                birthday_item = QTableWidgetItem(data[-1][2])
                wilaya_item = QTableWidgetItem(str(data[-1][3]))
                sex_item = QTableWidgetItem(str(data[-1][4]))
                allergies_item = QTableWidgetItem(data[-1][5])
                smoking_item = QTableWidgetItem(str(data[-1][6]))
                medhist_item = QTableWidgetItem(str(data[-1][7]))
                cancerf_item = QTableWidgetItem(str(data[-1][8]))
                eamil_item = QTableWidgetItem(str(data[-1][9]))
                phone_item = QTableWidgetItem(str(data[-1][10]))
                
                self.ui.tableWidget.setItem(row_count-1, 0, id_item)
                self.ui.tableWidget.setItem(row_count-1, 1, name_item)
                self.ui.tableWidget.setItem(row_count-1, 2, birthday_item)
                self.ui.tableWidget.setItem(row_count-1, 3, wilaya_item)
                self.ui.tableWidget.setItem(row_count-1, 4, sex_item)
                self.ui.tableWidget.setItem(row_count-1, 5, allergies_item)
                self.ui.tableWidget.setItem(row_count-1, 6, smoking_item)
                self.ui.tableWidget.setItem(row_count-1, 7, medhist_item)
                self.ui.tableWidget.setItem(row_count-1, 8, cancerf_item)
                self.ui.tableWidget.setItem(row_count-1, 9, eamil_item)
                self.ui.tableWidget.setItem(row_count-1, 10, phone_item)
                
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
    #? Select a file from the desktop
    def clicker(self):
        if self.PSelected == True:
            print("You clicked the button to choose a file !")
            fname = QFileDialog.getOpenFileName(self, "Open File and Choose the 3D Nodule", "" , "Python Files(*.npy)")
            self.scan = fname[0]
            if fname[0] !="" and fname[1] !="":
                self.Nodule3D = np.load(fname[0], allow_pickle=True)
                if self.Nodule3D.shape[0] == 64 and self.Nodule3D.shape[1] == 64 and self.Nodule3D.shape[2] == 64:
                    
                    #print(Nodule3D.shape)   
                    #plt.plot(Nodule3D[10,:,:,0])
                    #plt.show()
                    
                    #Clear the canvas 
                    self.figure.clear()
                    #plot
                    #im = Image.fromarray(Nodule3D[10,:,:,0])
                    #im.show()
                    #plt.imshow(Nodule3D[10,:,:,0],'gray')
                    self.ax1 = self.figure.add_subplot(self.grid[0, 0])
                    self.ax1.imshow(self.Nodule3D[32, :, :], cmap='gray')
                    self.ax1.set_title('Vue X')
                    self.ax2 = self.figure.add_subplot(self.grid[0, 1])
                    self.ax2.imshow(self.Nodule3D[:, 32, :], cmap='gray')
                    self.ax2.set_title('Vue Y')
                    self.ax3 = self.figure.add_subplot(self.grid[0, 2])
                    self.ax3.imshow(self.Nodule3D[:, :, 32], cmap='gray')
                    self.ax3.set_title('Vue Z')
                    #refresh
                    self.canvas.draw()
                else:
                    self.msg.setText("Please, select the right ct-scan  to start the classification.")
                    self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msg.exec_()
                    
            else:
                
                self.msg.setText("Please, select a ct-scan to start the classification, otherwise, no classification is possible")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
        else:
            self.msg.setText("Please, select a patient to start the classification.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
        
            
    #? Select a row from the table
    def handle_item_selection(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            self.PatientID = self.ui.tableWidget.item(selected_row, 0).text()
            self.PatientName = self.ui.tableWidget.item(selected_row, 1).text()
            print(self.PatientID)
    def PatientSelect(self):
        if self.PatientID != None:
            self.PSelected = True
            self.msg.setText("The patient named : "+self.PatientName+" has been selected.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
        else:
            self.msg.setText("Please, select a patient to start the classification.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            
            
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
        # Message
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Information")
        self.msg.setWindowIcon(QtGui.QIcon("ressources/logo.png"))
        #! Patient ID save and Name
        self.PatientID = None
        self.PatientName = ""
        # Patient bool selected
        self.PSelected = False
        # Fname
        self.scan= ""
        #expand center menu size
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        
        
        
        #Open file btn
        self.ui.openfileBtn.clicked.connect(self.clicker)
        
        #matplolib
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout(self.ui.frame_matplotlib)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        #canva
        self.figure = plt.figure()
        self.grid = GridSpec(1, 3)  # CrÃ©e une grille de 1 ligne et 3 colonnes pour les sous-graphiques
        

        self.canvas = FigureCanvas(self.figure)
        #end of canva
        
        #add canva
        self.horizontalLayout_44.addWidget(self.canvas)
        
    
        
        #close center menu 
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())
          
        #expand right menu size
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
     
        
        
        #close right menu 
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        
        #close Notification 
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())
        
        #close Notification 
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())
        
        # Classification
        self.ui.startClassificationBtn.clicked.connect(self.StartClassification)
        #Patient research
        self.ui.researchPatientBtn.clicked.connect(self.ResearchPatient)
        ##############################################################################################
        # No modification is allowed in the table
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.ui.label_addPName.hide()
        self.ui.label_addPWilaya.hide()
        self.ui.label_addPWilaya_2.hide()
        self.ui.label_addPSexe.hide()
        self.ui.label_addPAllergies.hide()
        self.ui.label_addPSmoking.hide()
        self.ui.label_addPMedHist.hide()
        self.ui.label_addPEmail.hide()
        self.ui.label_addPNumber.hide()
        
        self.ui.textNamePADD.hide()
        self.ui.textWilayaPADD.hide()
        self.ui.dateEditPADD.hide()
        self.ui.textSexePADD.hide()
        self.ui.textAllergiesPADD.hide()
        self.ui.textSmokingPADD.hide()
        self.ui.textMedHistPADD.hide()
        self.ui.textEmailPADD.hide()
        self.ui.textNumberPADD.hide()
        self.ui.tableWidget.hide()
        self.ui.addPateintBtn.hide()
        #!Add Patient
        self.ui.addPateintBtn.clicked.connect(self.AddPatient)
        #!Select a row from the table
        self.ui.tableWidget.itemSelectionChanged.connect(self.handle_item_selection)
        #! Choose patient
        self.ui.choosePateintBtn.clicked.connect(self.PatientSelect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())     