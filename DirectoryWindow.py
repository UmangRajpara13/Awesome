from PyQt5 import QtCore
from PyQt5 import QtWidgets
import os
from PyQt5.QtGui import QIcon
from AppsList import AllApps
from fbs_runtime.application_context.PyQt5 import ApplicationContext


class DirectoryWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(DirectoryWindow, self).__init__()
        self.parentWidget = parent
        self.resize(600, 400)
        self.setStyleSheet("background-color: #333;\n"
                           "color: #00FF00;\n"
                           "font-family: Courier;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.directoryList = QtWidgets.QListWidget(self.centralwidget)
        self.directoryList.setObjectName("directoryList")
        self.verticalLayout.addWidget(self.directoryList)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.removeDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.removeDirectory.setObjectName("removeDirectory")
        self.horizontalLayout.addWidget(self.removeDirectory)
        self.addDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.addDirectory.setObjectName("addDirectory")
        self.horizontalLayout.addWidget(self.addDirectory)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.removeDirectory.setText(_translate("MainWindow", "RemoveDirectory"))
        self.addDirectory.setText(_translate("MainWindow", "Add Directory"))
        self.SetupDirectoryList()
        self.directoryList.itemClicked.connect(self.GetSelection)
        self.addDirectory.clicked.connect(self.AddDir)
        self.removeDirectory.clicked.connect(self.RemoveDir)

    def SetupDirectoryList(self):
        for i in range(len(self.parentWidget.directoryList)):
            self.directoryList.addItem(self.parentWidget.directoryList[i])

    def AddDir(self):
        self.link = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.directoryList.addItem(self.link)
        self.parentWidget.directoryList.append(self.link)
        self.parentWidget.directories.addItem(self.link)
        self.parentWidget.UpdateDirectories()

    def RemoveDir(self):
        self.directoryList.takeItem(self.row)
        self.parentWidget.directoryList.pop(self.row)
        self.parentWidget.UpdateDirectories()

    def GetSelection(self, item):
        self.row = self.directoryList.row(item)
