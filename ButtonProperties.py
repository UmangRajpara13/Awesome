from PyQt5 import QtCore, QtWidgets


class ButtonProperties(QtWidgets.QMainWindow):
    def setupUi(self, parentWidget, buttonName):
        self.setObjectName("self")
        self.resize(468, 198)
        self.setStyleSheet("background-color: #333;\n"
                           "color: #00FF00;\n"
                           "font-family: Courier;")
        self.parentWidget = parentWidget
        self.buttonName = buttonName
        self.buttonIndex = self.parentWidget.buttonName.index(self.buttonName)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setObjectName("verticalFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.verticalFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.closeButton = QtWidgets.QPushButton(self.verticalFrame)
        self.closeButton.setObjectName("closeButton")

        self.closeButton.clicked.connect(self.Close)

        self.gridLayout.addWidget(self.closeButton, 4, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalFrame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalFrame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.moduleEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.moduleEdit.setObjectName("moduleEdit")

        self.moduleEdit.returnPressed.connect(self.Close)

        self.gridLayout.addWidget(self.moduleEdit, 1, 2, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.verticalFrame)
        self.saveButton.setObjectName("saveButton")

        self.saveButton.clicked.connect(self.Save)

        self.gridLayout.addWidget(self.saveButton, 4, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalFrame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.commandEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.commandEdit.setObjectName("commandEdit")

        self.commandEdit.returnPressed.connect(self.Close)

        self.gridLayout.addWidget(self.commandEdit, 3, 2, 1, 1)
        self.interpreterEdit = QtWidgets.QLineEdit(self.verticalFrame)
        self.interpreterEdit.setObjectName("interpreterEdit")

        self.interpreterEdit.returnPressed.connect(self.Close)

        self.gridLayout.addWidget(self.interpreterEdit, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.verticalFrame)
        self.setCentralWidget(self.centralwidget)

        try:
                self.LoadElements()
        except:
            message = '''There is somthing wrong with Json File for this App \n
                         you can fix it manually by editing Apps/'+self.parentWidget.appName+'/'+self.parentWidget.appName+'.json or,\n
                         visit www.Empower.com and download respective App Configuration(.json)'\n 
                         '''
            self.parentWidget.terminal.append(message)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Properties for " + "\'" + self.buttonName + "\'"))
        self.closeButton.setText(_translate("MainWindow", "Close"))
        self.label_3.setText(_translate("MainWindow", "Interpreter"))
        self.label.setText(_translate("MainWindow", "arg[1]/$1"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.label_2.setText(_translate("MainWindow", "Module"))

    def LoadElements(self):

        self.interpreterEdit.setText(self.parentWidget.buttonInterpreter[self.buttonIndex])
        self.moduleEdit.setText(self.parentWidget.buttonModule[self.buttonIndex])
        self.commandEdit.setText(self.parentWidget.buttonCommand[self.buttonIndex])


    def Close(self):
        self.Save()
        self.close()

    def Save(self):
        self.close()
        self.parentWidget.buttonInterpreter[self.buttonIndex] = self.interpreterEdit.text()
        self.parentWidget.buttonModule[self.buttonIndex] = self.moduleEdit.text()
        self.parentWidget.buttonCommand[self.buttonIndex] = self.commandEdit.text()
        self.parentWidget.Save()

