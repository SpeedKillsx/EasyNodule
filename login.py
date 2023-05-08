
from PyQt5 import QtCore, QtGui, QtWidgets
import sys,res
from sign import Ui_FormSign
from Database_methods import *
"""Tests:
- ClinicianLogin: work
- All the erros seems work well
- QMessageBoX must be checked after
"""
class Ui_Form(object):
        
        def openWindow(self):
                Form.close()
                self.window = QtWidgets.QWidget()
                self.ui = Ui_FormSign()
                self.ui.setupUi(self.window)
                self.window.show()
                
                
        def setupUi(self, Form):
                Form.setObjectName("Form")
                Form.resize(361, 460)
                Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                self.widget = QtWidgets.QWidget(Form)
                self.widget.setGeometry(QtCore.QRect(0, -10, 331, 451))
                self.widget.setStyleSheet("QPushButton#loginBtn,#signBtn{\n"
        "background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(20,47,78,219),stop:1 rgba(85,98,112,226));\n"
        "\n"
        "color:rgba(255,255,255,210);\n"
        "\n"
        "border-radius: 5px\n"
        "}\n"
        "\n"
        "QPushButton#loginBtn:hover{\n"
        "background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(40,67,98,219),stop:1 rgba(105,118,132,226));\n"
        "\n"
        "color:rgba(255,255,255,210);\n"
        "\n"
        "border-radius: 5px\n"
        "}\n"
        "QPushButton#signBtn:hover{\n"
        "background-color: qlineargradient(spread:pad,x1:0,y1:0.505682,x2:1,y2:0.477,stop:0 rgba(40,67,98,219),stop:1 rgba(105,118,132,226));\n"
        "\n"
        "color:rgba(255,255,255,210);\n"
        "\n"
        "border-radius: 5px\n"
        "}\n"
        "\n"
        "QPushButton#loginBtn,#signBtn:pressed{\n"
        "padding-left: 5px;\n"
        "padding-top: 5px;\n"
        "background-color : rgba(105,118,132,200);\n"
        "}\n"
        "\n"
        "\n"
        "QPushButton#emailBtn:pressed{\n"
        "padding-left: 5px;\n"
        "padding-top: 5px;\n"
        "background-color : rgba(105,118,132,200);\n"
        "}\n"
        "QPushButton#callBtn:pressed{\n"
        "padding-left: 5px;\n"
        "padding-top: 5px;\n"
        "background-color : rgba(105,118,132,200);\n"
        "}")
                self.widget.setObjectName("widget")
                self.label = QtWidgets.QLabel(self.widget)
                self.label.setGeometry(QtCore.QRect(30, 19, 300, 431))
                self.label.setStyleSheet("border-image: url(:/images/bg.jpg);\n"
        "border-radius : 20px;")
                self.label.setText("")
                self.label.setObjectName("label")
                self.label_2 = QtWidgets.QLabel(self.widget)
                self.label_2.setGeometry(QtCore.QRect(30, 19, 300, 431))
                self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:0.715909,stop:0.375 rgba(0,0,0,50),stop:0.835227 rgba(0,0,0,75));\n"
        "border-radius : 20px;")
                self.label_2.setText("")
                self.label_2.setObjectName("label_2")
                self.label_3 = QtWidgets.QLabel(self.widget)
                self.label_3.setGeometry(QtCore.QRect(40, 29, 280, 411))
                self.label_3.setStyleSheet("background-color: rgba(0,0,0,100);\n"
        "border-radius : 15px;")
                self.label_3.setText("")
                self.label_3.setObjectName("label_3")
                self.label_4 = QtWidgets.QLabel(self.widget)
                self.label_4.setGeometry(QtCore.QRect(80, 50, 91, 91))
                font = QtGui.QFont()
                font.setPointSize(20)
                font.setBold(True)
                font.setWeight(75)
                self.label_4.setFont(font)
                self.label_4.setStyleSheet("color: rgba(255,255,255,210);")
                self.label_4.setText("")
                self.label_4.setPixmap(QtGui.QPixmap(":/images/logo.png"))
                self.label_4.setScaledContents(True)
                self.label_4.setObjectName("label_4")
                self.usernameEdit = QtWidgets.QLineEdit(self.widget)
                self.usernameEdit.setGeometry(QtCore.QRect(80, 155, 200, 40))
                font = QtGui.QFont()
                font.setPointSize(10)
                self.usernameEdit.setFont(font)
                self.usernameEdit.setStyleSheet("background: rgba(0,0,0,0);\n"
        "border:0;\n"
        "border-bottom:2px solid rgba(105,118,132,255);\n"
        "color:rgba(255,255,255,230);\n"
        "padding-bottom:7px")
                self.usernameEdit.setObjectName("usernameEdit")
                self.passwordEdit = QtWidgets.QLineEdit(self.widget)
                self.passwordEdit.setGeometry(QtCore.QRect(80, 220, 200, 40))
                font = QtGui.QFont()
                font.setFamily("MS Shell Dlg 2")
                font.setPointSize(10)
                self.passwordEdit.setFont(font)
                self.passwordEdit.setStyleSheet("background: rgba(0,0,0,0);\n"
        "border:0;\n"
        "border-bottom:2px solid rgba(105,118,132,255);\n"
        "color:rgba(255,255,255,230);\n"
        "padding-bottom:7px")
                self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                self.passwordEdit.setObjectName("passwordEdit")
                self.loginBtn = QtWidgets.QPushButton(self.widget)
                self.loginBtn.setGeometry(QtCore.QRect(80, 290, 200, 40))
                font = QtGui.QFont()
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.loginBtn.setFont(font)
                self.loginBtn.setObjectName("loginBtn")
                self.label_5 = QtWidgets.QLabel(self.widget)
                self.label_5.setGeometry(QtCore.QRect(180, 90, 101, 21))
                font = QtGui.QFont()
                font.setPointSize(12)
                font.setBold(True)
                font.setWeight(75)
                self.label_5.setFont(font)
                self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
                self.label_5.setObjectName("label_5")
                self.label_6 = QtWidgets.QLabel(self.widget)
                self.label_6.setGeometry(QtCore.QRect(90, 370, 191, 21))
                self.label_6.setStyleSheet("color: rgba(255,255,255,140);")
                self.label_6.setObjectName("label_6")
                self.emailBtn = QtWidgets.QPushButton(self.widget)
                self.emailBtn.setGeometry(QtCore.QRect(140, 400, 31, 30))
                self.emailBtn.setMinimumSize(QtCore.QSize(30, 30))
                font = QtGui.QFont()
                font.setPointSize(15)
                self.emailBtn.setFont(font)
                self.emailBtn.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
        "")
                self.emailBtn.setText("")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/images/gmail.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.emailBtn.setIcon(icon)
                self.emailBtn.setIconSize(QtCore.QSize(24, 24))
                self.emailBtn.setObjectName("emailBtn")
                self.callBtn = QtWidgets.QPushButton(self.widget)
                self.callBtn.setGeometry(QtCore.QRect(200, 400, 31, 30))
                self.callBtn.setMinimumSize(QtCore.QSize(30, 30))
                font = QtGui.QFont()
                font.setPointSize(15)
                self.callBtn.setFont(font)
                self.callBtn.setStyleSheet("background-color: rgba(0, 0, 0,0);")
                self.callBtn.setText("")
                icon1 = QtGui.QIcon()
                icon1.addPixmap(QtGui.QPixmap(":/images/appel-telephonique.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.callBtn.setIcon(icon1)
                self.callBtn.setIconSize(QtCore.QSize(24, 24))
                self.callBtn.setObjectName("callBtn")
                self.label_7 = QtWidgets.QLabel(self.widget)
                self.label_7.setGeometry(QtCore.QRect(90, 350, 81, 21))
                self.label_7.setStyleSheet("color: rgba(255,255,255,140);")
                self.label_7.setObjectName("label_7")
                self.signBtn = QtWidgets.QPushButton(self.widget , clicked = lambda : self.openWindow())
                self.signBtn.setGeometry(QtCore.QRect(180, 350, 51, 20))
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(True)
                font.setWeight(75)
                self.signBtn.setFont(font)
                self.signBtn.setObjectName("signBtn")
                
                self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius = 25 , xOffset=0 , yOffset = 0,color = QtGui.QColor(234,221,186,100)))
                self.label_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius = 25 , xOffset=0 , yOffset = 0,color = QtGui.QColor(105,118,132,100)))
                self.loginBtn.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius = 25 , xOffset=3 , yOffset = 3,color = QtGui.QColor(105,118,132,100)))
                
                self.msg = QtWidgets.QMessageBox()
                
                self.msg.setWindowTitle("Information")
                self.msg.setWindowIcon(QtGui.QIcon("ressources/logo.png"))
                #self.msg.setStyleSheet("border-image: url(:/images/bg.jpg);")
                
                
                self.retranslateUi(Form)
                QtCore.QMetaObject.connectSlotsByName(Form)
                #print(self.usernameEdit.text())
                self.loginBtn.clicked.connect(self.ClinicianLogin)
                

        def retranslateUi(self, Form):
                _translate = QtCore.QCoreApplication.translate
                Form.setWindowTitle(_translate("Form", "Form"))
                self.usernameEdit.setPlaceholderText(_translate("Form", "User Name"))
                self.passwordEdit.setPlaceholderText(_translate("Form", "Password"))
                self.loginBtn.setText(_translate("Form", "L o g  In"))
                self.label_5.setText(_translate("Form", "Easy Nodule"))
                self.label_6.setText(_translate("Form", "Forgot your User Name Or Password ?"))
                self.label_7.setText(_translate("Form", "Not a member ?  "))
                self.signBtn.setText(_translate("Form", "sign in"))
        
        
        
        #* UI methods
        def ClinicianLogin(self):
                
                print("ici")
                if self.usernameEdit.text()=="" or self.passwordEdit.text()=="":
                        #print("Please fill all the fields")
                        self.msg.setText("Please fill all the fields")
                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msg.exec_()
                elif ClinicianResearch(self.usernameEdit.text(),self.passwordEdit.text()) == -1:
                        #print("No account with this ID!!!!")
                        self.msg.setText("Username or password are incorrect")
                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msg.exec_()
                else:
                        #print("You are connected now")
                        self.msg.setText("You are connected.\nWelcome again")
                        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msg.exec_()
                        
                        
if __name__ == "__main__":
        app=QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()
        
        sys.exit(app.exec_())
