import os
import sys
from PySide2 import *
from GUI.interface_ui import *
from utils.invoice import MakePDF
from Custom_Widgets.Widgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import numpy as np
from PIL import Image
from utils.Preporcessing import *
from utils.Database_methods import *
import pygame
import sqlite3
import re
class MainWindow(QMainWindow):
    #! Ajout de la verification de email
    def isValid(self, email):
        regex = re.compile(r"^\w+@\w+\.\w+$")
        if re.fullmatch(regex, email):
            return 1
        else:
            return 0

    def LoadModels(self):
        path_modelX = "Models\capsule-X"
        path_modelY = "Models\capsule-Y"
        path_modelZ = "Models\capsule-Z"
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
            self.ui.label_waiting.show()
            #! Load all models
            self.LoadModels()
            #! Make a prediction
            if (self.ClassMethode == 0):
                print("major")
                classification = final_predMAJOR(self.Nodule3D[:,:,32], self.Nodule3D[:,32,:],self.Nodule3D[32,:,:],self.ModelX,self.ModelY,self.ModelZ)
            if (self.ClassMethode == 1):
                print("seuil")
                classification = final_pred(self.Nodule3D[:,:,32], self.Nodule3D[:,32,:],self.Nodule3D[32,:,:],self.ModelX,self.ModelY,self.ModelZ)
            if (self.ClassMethode == 2):
                print("thj")
                classification = thj_pred(self.Nodule3D[:,:,32], self.Nodule3D[:,32,:],self.Nodule3D[32,:,:],self.ModelX,self.ModelY,self.ModelZ)
            if (self.ClassMethode == 3):
                print("strict")
                classification = final_predSTRICT(self.Nodule3D[:,:,32], self.Nodule3D[:,32,:],self.Nodule3D[32,:,:],self.ModelX,self.ModelY,self.ModelZ)
            
            result = None
            if classification == 0:
                result="The nodule is Benin"
                self.ModelResult = "Benin"
            else:
                result="The nodule is Malignant"
                self.ModelResult = "Malignant"
            print(result)
            
            # Charger le fichier audio
            pygame.mixer.music.load("ressources/notificationsound.mp3")

            # Lancer la lecture
            pygame.mixer.music.play()
            self.ui.label_13.setText("The nodule classification is complete.")
            #self.ui.popupNotificationSubContainer.show()
            self.ui.notificationBtn.click()
            #####################################################################################################
            self.ui.textRPname.setText(self.PatientName)
            self.ui.textRPage.setText(self.PatientBirthday)
            self.ui.textRPwilaya.setText(self.PatientWilaya)
            self.ui.textRPsexe.setText(self.PatientSexe)
            self.ui.textRPemail.setText(self.PatientEmail)
            self.ui.textRPphone.setText(self.PatientPhone)
            self.ui.textRPallergies.setText(self.PatientAllergies)
            self.ui.textRPsmoking.setText(self.PatientSmoking)
            self.ui.textRPmedhist.setText(self.PatientMedHist)
            
            self.ui.textRModelClassification.setText(self.ModelResult)
            #self.ui.label_13.setText("Notification message")
            
            
            
            #####################################################################################################
            self.ui.label_waiting.hide()  
            ##! X Classification
            prX, valX = predict_proba(self.ModelX,tf.expand_dims(Preprocessing(self.Nodule3D[:,:,32]),0))
            #print(valX[0])
            if(valX[0] == 0):
                self.ui.textXClasse.setText("Benin")
                #print("X benin")
            else:
                self.ui.textXClasse.setText("Malignant")
                #print("Xmalin")
            prX = prX.numpy()
            #print(prX)
            #print("PRCG X  ",round(np.max(prX)*100,2))
            self.ui.textXPctg.setText(str(round(np.max(prX)*100,2)))
            
            ##! Y Classification
            prY, valY = predict_proba(self.ModelY,tf.expand_dims(Preprocessing(self.Nodule3D[:,32,:]),0))
            if(valY[0] == 0):
                self.ui.textYClasse.setText("Benin")
            else:
                self.ui.textYClasse.setText("Malignant")
            prY = prY.numpy() 
            self.ui.textYPctg.setText(str(round(np.max(prY)*100,2)))
            ##! Z Classification
            prZ, valZ = predict_proba(self.ModelZ,tf.expand_dims(Preprocessing(self.Nodule3D[32,:,:]),0))
            if(valZ[0] == 0):
                self.ui.textZClasse.setText("Benin")
            else:
                self.ui.textZClasse.setText("Malignant")
            
            prZ = prZ.numpy() 
            self.ui.textZPctg.setText(str(round(np.max(prZ)*100,2)))
            self.ui.textFinalClassification.setText(result)
            #self.PatientID = ""
            #self.PSelected = False
            self.GlobalStartClassification = 1
            print("self.GlobalStartClassification = ", self.GlobalStartClassification)
            
            
        else:
            if self.scan == "":
                self.ui.label_waiting.hide()  
                self.msg.setText("Please, select the right ct-scan  to start the classification.")
                self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msg.exec_()
            else:    
                #! Patient ID save and Name and all information
                self.PatientID = None
                self.PatientName = ""
                self.PatientWilaya = ""
                self.PatientBirthday = ""
                self.PatientSexe = ""
                self.PatientAllergies = ""
                self.PatientSmoking = ""
                self.PatientCancerFamilly = ""
                self.PatientMedHist = ""
                self.PatientEmail = ""
                self.PatientPhone = ""
                #ModelResult
                self.ModelResult =""
                self.ui.label_waiting.hide()  
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
        self.ui.label_addPCancerFamilly.show()
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
        self.ui.textCancerFamillyPADD.show()
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
        self.ui.label_addPCancerFamilly.hide()
        self.ui.label_addPMedHist.hide()
        self.ui.label_addPEmail.hide()
        self.ui.label_addPNumber.hide()
        
        self.ui.textNamePADD.hide()
        self.ui.textWilayaPADD.hide()
        self.ui.dateEditPADD.hide()
        self.ui.textSexePADD.hide()
        self.ui.textAllergiesPADD.hide()
        self.ui.textSmokingPADD.hide()
        self.ui.textCancerFamillyPADD.hide()
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
            self.selected_wilaya = self.ui.textWilayaPADD.itemText(self.ui.textWilayaPADD.currentIndex())
            self.selected_sex = self.ui.textSexePADD.itemText(self.ui.textSexePADD.currentIndex()) 
            self.selected_smok = self.ui.textSmokingPADD.currentIndex()
            self.selected_CancerF = self.ui.textCancerFamillyPADD.currentIndex()
            print(self.selected_wilaya)
            if(self.ui.textNamePADD.toPlainText()!="" and self.ui.dateEditPADD.text()!="" and self.ui.textAllergiesPADD.toPlainText()!="" and self.ui.textMedHistPADD.toPlainText()!=""and self.ui.textEmailPADD.toPlainText()!="" and self.ui.textNumberPADD.toPlainText() !=""):
                    if len(self.ui.textNumberPADD.toPlainText()) == 10:
                        if self.isValid(self.ui.textEmailPADD.toPlainText()) == 1:
                            #value_familly = 0  
                            PatientInsert(self.ui.textNamePADD.toPlainText(),
                                        self.ui.dateEditPADD.text(),
                                        self.selected_wilaya,
                                        self.selected_sex,
                                        self.ui.textAllergiesPADD.toPlainText(),
                                        self.selected_smok,
                                        self.ui.textMedHistPADD.toPlainText(),
                                        self.selected_CancerF,
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
                            self.ui.label_addPCancerFamilly.hide()
                            self.ui.label_addPMedHist.hide()
                            self.ui.label_addPEmail.hide()
                            self.ui.label_addPNumber.hide()
                            
                            self.ui.textNamePADD.hide()
                            self.ui.textWilayaPADD.hide()
                            self.ui.dateEditPADD.hide()
                            self.ui.textSexePADD.hide()
                            self.ui.textAllergiesPADD.hide()
                            self.ui.textSmokingPADD.hide()
                            self.ui.textCancerFamillyPADD.hide()
                            self.ui.textMedHistPADD.hide()
                            self.ui.textEmailPADD.hide()
                            self.ui.textNumberPADD.hide()
                            self.add_data()
                            self.msg.setText("Patient added succefully.")
                            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            self.msg.exec_()
                            self.selected_wilaya = "Adrar"
                            self.selected_sex = "Male"
                            self.selected_smok = 0
                            self.selected_CancerF= 0
                            
                            self.ui.textWilayaPADD.setCurrentIndex(0)
                            self.ui.textSexePADD.setCurrentIndex(0)
                            self.ui.textSmokingPADD.setCurrentIndex(0)
                            self.ui.textCancerFamillyPADD.setCurrentIndex(0)
                            
                            
                            self.ui.textNamePADD.clear()
                            #self.ui.textWilayaPADD.hide()
                            self.ui.dateEditPADD.setDate(QDate(2000, 1, 1))
                            #self.ui.textSexePADD.hide()
                            self.ui.textAllergiesPADD.clear()
                            #self.ui.textSmokingPADD.hide()
                            #self.ui.textCancerFamillyPADD.hide()
                            self.ui.textMedHistPADD.clear()
                            self.ui.textEmailPADD.clear()
                            self.ui.textNumberPADD.clear()
                        else:
                            self.msg.setText("Incorrect email !")
                            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            self.msg.exec_()
                    else:
                        
                        self.msg.setText("Incorrect phone number !")
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
            
    #? Print data in the table, (errnigh l affichage nni g tableau)
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
            if str(data[6]) == "0":
                smoking_item = QTableWidgetItem("No")
            else:
                smoking_item = QTableWidgetItem("Yes")
            medhist_item = QTableWidgetItem(str(data[7]))
            if str(data[8]) == "0":
                cancerf_item = QTableWidgetItem("No")
            else:
                cancerf_item = QTableWidgetItem("Yes")
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
                    if str(data[i][6]) == "0":
                        smoking_item = QTableWidgetItem("No")
                    else:
                        smoking_item = QTableWidgetItem("Yes")
                    medhist_item = QTableWidgetItem(str(data[i][7]))
                    if str(data[i][8]) == "0":
                        cancerf_item = QTableWidgetItem("No")
                    else:
                        cancerf_item = QTableWidgetItem("Yes")
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
            print("hh ",fname[0])
            if fname[0] !="" and fname[1] !="":
                self.Nodule3D = np.load(fname[0],allow_pickle=True)
                print("shape ",self.Nodule3D.shape)
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
        
           
    #? Select a row from the table (modifyight i la citte)
    def handle_item_selection(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            if self.ui.tableWidget.item(selected_row, 0) is not None:
                
                self.PatientID = self.ui.tableWidget.item(selected_row, 0).text()
                self.PatientName = self.ui.tableWidget.item(selected_row, 1).text()
                self.PatientWilaya = self.ui.tableWidget.item(selected_row, 3).text()
                self.PatientBirthday = self.ui.tableWidget.item(selected_row, 2).text()
                self.PatientSexe = self.ui.tableWidget.item(selected_row, 4).text()
                self.PatientAllergies = self.ui.tableWidget.item(selected_row, 5).text()
                self.PatientSmoking = self.ui.tableWidget.item(selected_row, 6).text()
                self.PatientCancerFamilly = self.ui.tableWidget.item(selected_row, 8).text()
                self.PatientMedHist = self.ui.tableWidget.item(selected_row, 7).text()
                self.PatientEmail = self.ui.tableWidget.item(selected_row, 9).text()
                self.PatientPhone = self.ui.tableWidget.item(selected_row, 10).text()
                print(self.PatientID)
                self.PatientIDTemp = self.PatientID
                self.PatientNameTemp = self.PatientName
            else:
                self.msg.setText("Please choose a patient from the table")
                self.msg.exec_()
    def PatientSelect(self):
        if self.PatientID != "":
            self.PSelected = True
            self.msg.setText("The patient named : "+self.PatientName+" has been selected.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            self.GlobalStartClassification = 0
        else:
            self.msg.setText("Please, select a patient to start the classification.")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.exec_()
            
    def ChooseClassificationMethode(self):
        if self.ui.radioMajor.isChecked() :
            self.ClassMethode = 0 
            self.ui.label_CM.setText("Majority")
        if self.ui.radioThresholding.isChecked() :
            self.ClassMethode = 1
            self.ui.label_CM.setText("Thresholding")
        if self.ui.radioGameTheory.isChecked() :
            self.ClassMethode = 2
            self.ui.label_CM.setText("Game Theory")
        if self.ui.radioStrict.isChecked() :
            self.ClassMethode = 3  
            self.ui.label_CM.setText("Strict")
            
    
        print("methode ",self.ClassMethode)          
    def showNodule(self):
        temp = self.scan
        import subprocess
        command = 'utils/contours.py ' # Remplacez 'dir' par la commande de votre choix
        # Exécute la commande CMD et récupère la sortie
        #! Check if a ct-scan file was selected
        if self.scan !="":
            subprocess.Popen(["python", command, temp])
        else:
            self.msg.setText("No CT-scan selected ! \nPlease select a valid CT-scan file and start the classification process, then you can visulalize the nodule.")
            self.msg.exec_()
    
    
    def NodClassification(self):
        self.ui.label_waiting.setText("Please wait !")
        self.ui.label_13.setText("The Nodule Classification is complete !")
        self.StartClassification()  
        self.ui.label_waiting.setText("")  
    
    def get_statistics(self):
        self.conn = sqlite3.connect("utils/NoduleDataBase.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT WilayaP, COUNT(*) FROM Patient WHERE idP in (SELECT idP from Nodule where NoduleClassification == '1') GROUP BY WilayaP")
        results = self.cursor.fetchall()

        # Générer les statistiques sous forme de dictionnaire
        stats = {result[0]: result[1] for result in results}
        self.conn.close()
        return stats
    def update_graph(self):
        self.conn = sqlite3.connect("utils/NoduleDataBase.db")
        self.cursor = self.conn.cursor()
        # Récupérer les données de la base de données
        self.cursor.execute("""
            SELECT Patient.Allergies, Nodule.NoduleClassification, Patient.Smoking, Patient.CancerFamilly, Patient.MedHistory
            FROM Patient
            INNER JOIN Nodule ON Patient.idP = Nodule.idP
        """)
        data = self.cursor.fetchall()

        # Préparer les variables pour la représentation graphique
        allergies_malignant = 0
        allergies_benign = 0
        smoking_malignant = 0
        smoking_benign = 0
        cancer_family_positive = 0
        cancer_family_negative = 0
        med_history_none = 0
        med_history_diseases = 0
        # POur chaque ligne dans la base de données, on effectue differents tests
        for row in data:
            allergy, malignant, smoking, cancer_family, med_history = row
            #! Cas allergy
            if allergy.upper()!='NONE':
                if malignant == 1:
                    allergies_malignant += 1
            else:
                if malignant == 1:
                    allergies_benign += 1
            #! Cas smoking
            if smoking == 1:
                if malignant == 1:
                    smoking_malignant += 1
            else:
                if malignant == 1:
                    smoking_benign += 1
            #! Cas Cancer Famillly
            if cancer_family == 1:
                if malignant == 1:
                    cancer_family_positive += 1
            else:
                if malignant == 1:
                    cancer_family_negative += 1
            #! Cas medical history
            if med_history.upper()!="NONE":
                if malignant == 1:
                    med_history_diseases += 1
            else:
                if malignant == 1:
                    med_history_none += 1

        # Créer le graphique
        malignant_values = [allergies_malignant, smoking_malignant, cancer_family_positive, med_history_diseases]
        benign_values = [allergies_benign, smoking_benign, cancer_family_negative, med_history_none]
        self.conn.close()
        return malignant_values,benign_values

    def maj_stat(self):
        
        
        
       
        # Obtenir les statistiques à partir de la base de données
        self.stats = self.get_statistics()
        
        self.ax.clear()
        self.wedges, self.labels, self.autotexts = self.ax.pie(self.stats.values(), autopct="%1.1f%%", startangle=90)
        self.ax.axis("equal")

        # Ajouter les légendes
        self.ax.legend(self.wedges, self.stats.keys(), title="Wilaya", loc="center left", bbox_to_anchor=(0.87, 0.5))
        
        self.canvasstat1.draw()
        
        ###########################################################################################################
        #! Ajoute le 19/06/2023 a 23h26
        self.malignant_values, self.benign_values = self.update_graph()
        self.ax2.clear()
        self.ax2.bar(self.ind - self.width/2, self.malignant_values, self.width, color='red', label='Positive')
        self.ax2.bar(self.ind + self.width/2, self.benign_values, self.width, color='blue', label='Negative')
        self.ax2.set_xlabel('Categories', color="white")
        self.ax2.set_ylabel('Values', color="white")
        #self.ax2.set_title('Statistics', color="white")
        self.ax2.set_xticks(self.ind)
        self.ax2.set_xticklabels(self.categories, color="yellow")
        self.ax2.tick_params(axis='y', colors='white')
        self.ax2.legend()

        self.canvasstat2.draw()
    def saveReport(self):
        #! si le nom est ecrit dans son champ (ajt le 16/06/2023)
        if self.ui.textRPname !="":
            #! Ajouter la condition si le path n est pas vide
            if self.scan !="" and self.ui.plainTextEdit.toPlainText()!="":
                #! Ajouter la condition si une classification a ete effectue
                if self.GlobalStartClassification == 1:
                    self.GlobalStartClassification = 0
                    self.Cid = self.ui.textIdC.toPlainText()
                    self.Cname = self.ui.textNameC.toPlainText()
                    print("hellow = ", self.Cid,self.Cname, self.PatientIDTemp)
                    #ICI On Ajoute a la BDD Consultation et on récupère IdConsultation
                    
                    #self.CSid ="PS44740"
                    #ICI On Ajoute a la BDD Consultation et on récupère IdConsultation
                    if self.PatientIDTemp!="":
                        if SearchConsultation(self.Cid, self.PatientIDTemp,datetime.date.today()) == -1:
                            ConsultationInsert(self.Cid, self.PatientIDTemp, datetime.date.today(), self.ui.plainTextEdit.toPlainText())
                            self.CSid = ConsultationID(self.PatientIDTemp, self.Cid, datetime.date.today())
                            print("csid = ", self.CSid[0])
                            
                            #!! Ici je vais faire une modif, je vais inserer juste la le nodule
                            self.msg.setText("Consultation added succefully")
                            self.msg.exec_()
                            if((self.ui.textRPname.toPlainText() != "") and (self.ui.plainTextEdit.toPlainText() != "")):
                                #print("oui")
                                """if self.ui.textRModelClassification.toPlainText() =="Benin":
                                    NoduleInsert(self.CSid[0], self.PatientIDTemp, np.load(self.scan, allow_pickle=True),0)
                                    self.msg.setText("nodule added succefully")
                                    self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                    self.msg.exec_()
                                else:
                                    NoduleInsert(self.CSid[0], self.PatientIDTemp, np.load(self.scan, allow_pickle=True),1)
                                    self.msg.setText("nodule added succefully")
                                    
                                    self.msg.exec_()"""
                                if NoduleResearch(self.CSid[0]) == 1:
                                        self.msg.setText("The Nodule Existe")
                                        self.msg.exec_()
                                else:
                                    
                                    if(self.ui.radioNBenin.isChecked()):
                                        #! Check if the nodule was aded before 
                                        print("CSID dans save report = ", self.CSid[0])
                                        
                                        #! Add nodule to the database
                                        NoduleInsert(self.CSid[0], self.PatientIDTemp, np.load(self.scan, allow_pickle=True),0)
                                        self.msg.setText("Nodule added succefully")
                                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                        self.msg.exec_()
                                        MakePDF(self.ui.textRPname.toPlainText(), self.CSid[0] , self.PatientID ,self.ui.textRPwilaya.toPlainText() ,  self.ui.textRPphone.toPlainText() , self.ui.textRPemail.toPlainText(), self.ui.textRModelClassification.toPlainText() , "Benin" , self.ui.plainTextEdit.toPlainText() , self.Cname , self.Cid) 
                                        self.msg.setText("Your Report is saved correctly !")
                                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                        self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
                                        #* Ajout de ces deux lignes pour rafraichir le canevas (12/06/2023)
                                        self.figure.clear()
                                        self.canvas.draw()
                                        self.scan = ""
                                        #! Mise a blanc des champs (Ajoute le vendredi 16/06/2023)
                                        self.ui.textRPname.setText("")
                                        self.ui.textRPage.setText("")
                                        self.ui.textRPwilaya.setText("")
                                        self.ui.textRPsexe.setText("")
                                        self.ui.textRPemail.setText("")
                                        self.ui.textRPphone.setText("")
                                        self.ui.textRPallergies.setText("")
                                        self.ui.textRPsmoking.setText("")
                                        self.ui.textRPmedhist.setText("")
                                        self.ui.textRModelClassification.setText("")
                                        self.ui.plainTextEdit.clear()
                                        
                                    elif(self.ui.radioNMalignant.isChecked()):
                                        #! Add nodule to the database
                                        NoduleInsert(self.CSid[0], self.PatientIDTemp, np.load(self.scan, allow_pickle=True),1)
                                        self.msg.setText("Nodule added succefully")
                                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                        self.msg.exec_()
                                        MakePDF(self.ui.textRPname.toPlainText(), self.CSid[0] , self.PatientID ,self.ui.textRPwilaya.toPlainText() ,  self.ui.textRPphone.toPlainText() , self.ui.textRPemail.toPlainText(), self.ui.textRModelClassification.toPlainText() , "Malignant" , self.ui.plainTextEdit.toPlainText() , self.Cname , self.Cid) 
                                        self.msg.setText("Your Report is saved correctly !")
                                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                        self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
                                        #* Ajout de ces deux lignes pour rafraichir le canevas (12/06/2023)
                                        self.figure.clear()
                                        self.canvas.draw()
                                        self.scan=""
                                        #! Mise a blanc des champs (Ajoute le vendredi 16/06/2023)
                                        self.ui.textRPname.setText("")
                                        self.ui.textRPage.setText("")
                                        self.ui.textRPwilaya.setText("")
                                        self.ui.textRPsexe.setText("")
                                        self.ui.textRPemail.setText("")
                                        self.ui.textRPphone.setText("")
                                        self.ui.textRPallergies.setText("")
                                        self.ui.textRPsmoking.setText("")
                                        self.ui.textRPmedhist.setText("")
                                        self.ui.textRModelClassification.setText("")
                                        self.ui.plainTextEdit.clear()
                                    else:
                                        self.msg.setText("Please, Select your Classification methode !")
                                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                                        self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
                        else :
                            #* Modification le 12/06/2023, modification du message
                            self.msg.setText("Consultation is not added, please check out the patient's information or maybe you already passed a consultation for this patient!\n ")
                            self.msg.exec_()
                            ###################################################################
                            #Radio
                    else:
                        self.msg.setText("Please check your informations")
                        self.msg.exec_()
                    #!! aavant Ici j avais inserer juste la le nodule
                else:
                    self.msg.setText("You must start the classification process before creating your report !")
                    self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
            else:
                #! Cas ou le chemin est vide 
                if self.scan == "":    
                    self.msg.setText("You must start the classification process before creating your report !")
                    self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
                else:
                    self.msg.setText("You must give your feedback in order to save the report.")
                    self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.msg.exec_()    #print(self.ui.textRPname.toPlainText())
        else:
            self.msg.setText("Please check out the patient's information")
            self.msg.exec_()
                
            
                
                
    def selection_changed(self, index):
        self.selected_wilaya = self.ui.textWilayaPADD.itemText(index)
        print("Wilaya sélectionnée :", self.selected_wilaya)
        
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
        # Initialiser pygame
        pygame.init()
        # Message
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("Information")
        self.msg.setWindowIcon(QtGui.QIcon("ressources/logo.png"))
        #! Patient ID save and Name and all information
        self.PatientID = ""
        self.PatientIDTemp = ""
        self.PatientName = ""
        self.PatientNameTemp = ""
        self.PatientWilaya = ""
        self.PatientBirthday = ""
        self.PatientSexe = ""
        self.PatientAllergies = ""
        self.PatientSmoking = ""
        self.PatientCancerFamilly = ""
        self.PatientMedHist = ""
        self.PatientEmail = ""
        self.PatientPhone = ""
        #! Ajout de la wilaya selectionnee
        self.selected_wilaya = "Adrar"
        self.selected_sex = "Male"
        self.selected_smok = 0
        self.selected_CancerF= 0
        #ModelResult
        self.ModelResult =""
        # Patient bool selected
        self.PSelected = False
        # Fname
        self.scan= ""
        #Clinicien Info et id consultation
        self.Cname = ""
        self.Cid = ""
        self.CSid = ""
        #Classification méthode
        self.ClassMethode = 0
        
        #expand center menu size
        self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        
        
        
        #Open file btn
        self.ui.openfileBtn.clicked.connect(self.clicker)
        
        #maj Stat
        self.ui.statBtn.clicked.connect(self.maj_stat)
        
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
        
        #matplolibStat
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout(self.ui.frame_stat1)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        #canva
        self.figurestat1 = plt.figure()

        self.canvasstat1 = FigureCanvas(self.figurestat1)
        #end of canva
        
        #add canva
        self.horizontalLayout_55.addWidget(self.canvasstat1)
        
        # Se connecter à la base de données
        self.conn = sqlite3.connect("utils/NoduleDataBase.db")
        self.cursor = self.conn.cursor()
        # Obtenir les statistiques à partir de la base de données
        self.stats = self.get_statistics()

        # Créer un graphique camembert
        self.ax = self.figurestat1.add_subplot(111)
        self.wedges, self.labels, self.autotexts = self.ax.pie(self.stats.values(), autopct="%1.1f%%", startangle=90)
        self.ax.axis("equal")

        # Ajouter les légendes
        self.ax.legend(self.wedges, self.stats.keys(), title="Wilaya", loc="center left", bbox_to_anchor=(0.87, 0.5))
        
        
        #matplolibStat
        self.horizontalLayout_66 = QtWidgets.QHBoxLayout(self.ui.frame_stat2)
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        #canva
        self.figurestat2 = plt.figure()
        self.canvasstat2 = FigureCanvas(self.figurestat2)
        #end of canva
        self.horizontalLayout_66.addWidget(self.canvasstat2)

        # Créer le graphique
        self.categories = ['Allergies', 'Smoking', 'CancerFamilly', 'MedHistory']
        self.malignant_values, self.benign_values = self.update_graph()

        self.figurestat2.set_facecolor("none")
        self.ax2 = self.figurestat2.add_subplot(111)
        self.ind = np.arange(len(self.categories))
        self.width = 0.35
        self.ax2.bar(self.ind - self.width/2, self.malignant_values, self.width, color='red', label='Positive')
        self.ax2.bar(self.ind + self.width/2, self.benign_values, self.width, color='blue', label='Negative')
        self.ax2.set_xlabel('Categories', color="white")
        self.ax2.set_ylabel('Values', color="white")
        #self.ax2.set_title('Statistics', color="white")
        self.ax2.set_xticks(self.ind)
        self.ax2.set_xticklabels(self.categories, color="yellow")
        self.ax2.tick_params(axis='y', colors='white')
        self.ax2.legend()

        self.canvasstat2.draw()
        self.horizontalLayout_66.addWidget(self.canvasstat2)
        self.conn.close()
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
        self.ui.startClassificationBtn.clicked.connect(self.NodClassification)
        #Patient research
        self.ui.researchPatientBtn.clicked.connect(self.ResearchPatient)
        ##############################################################################################
        # No modification is allowed in the table
        self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Patient ID", "Name", "Birth", "Wilaya", "Sex", "Allergies", "Smoking", "Medical history", "Cancer Family", "Email", "Phone"])
        # Personnalisation du style des titres de colonnes
        header_style = "::section { background-color: #333; color: white; }"
        self.ui.tableWidget.horizontalHeader().setStyleSheet(header_style)
        
        self.ui.label_addPName.hide()
        self.ui.label_addPWilaya.hide()
        self.ui.label_addPWilaya_2.hide()
        self.ui.label_addPSexe.hide()
        self.ui.label_addPAllergies.hide()
        self.ui.label_addPSmoking.hide()
        self.ui.label_addPCancerFamilly.hide()
        self.ui.label_addPMedHist.hide()
        self.ui.label_addPEmail.hide()
        self.ui.label_addPNumber.hide()
        
        self.ui.textNamePADD.hide()
        self.ui.textWilayaPADD.hide()
        self.ui.dateEditPADD.hide()
        self.ui.textSexePADD.hide()
        self.ui.textAllergiesPADD.hide()
        self.ui.textSmokingPADD.hide()
        self.ui.textCancerFamillyPADD.hide()
        self.ui.textMedHistPADD.hide()
        self.ui.textEmailPADD.hide()
        self.ui.textNumberPADD.hide()
        self.ui.tableWidget.hide()
        self.ui.addPateintBtn.hide()
        #* Ajout d une variable globale pour gerer le cas ou un pdf se cree si aucune consultation n a ete effectuee
        self.GlobalStartClassification = 0
        #!Add Patient
        self.ui.addPateintBtn.clicked.connect(self.AddPatient)
        #!Select a row from the table
        self.ui.tableWidget.itemSelectionChanged.connect(self.handle_item_selection)
        #! Choose patient
        self.ui.choosePateintBtn.clicked.connect(self.PatientSelect)
        
        #hide waiting
        self.ui.label_waiting.setText("")
        
        #Save report
        self.ui.saveReportBtn.clicked.connect(self.saveReport)
        # Show nodule
        self.ui.showNoduleRBtn.clicked.connect(self.showNodule)
        # Choose classification methode
        self.ui.classificationMethodeBtn.clicked.connect(self.ChooseClassificationMethode)
        
        #
        self.ui.textBrowserGuide.setOpenExternalLinks(True)
        self.ui.textBrowserGuide.append('<a href=https://drive.google.com/file/d/1hkQrMOivxnh7-qVpXAUndPckf9Svx9ts/view?usp=share_link>MethodesPdf</>')
        
        self.ui.textBrowserGuidePDF.setOpenExternalLinks(True)
        self.ui.textBrowserGuidePDF.append('<a href=https://drive.google.com/file/d/17CHbUR6hFuHHutq4315FIcD0YL-yEEI3/view?usp=sharing>______Guide_____</>')
        #self.ui.textWilayaPADD.currentIndexChanged.connect(self.selection_changed)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set the application icon
    app.setWindowIcon(QIcon('ressources/logo.png'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())     