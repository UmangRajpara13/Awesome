from PyQt5 import QtCore
from PyQt5 import QtWidgets
import os
from PyQt5.QtGui import QIcon
from AppsList import AllApps
from fbs_runtime.application_context.PyQt5 import ApplicationContext


class Ui_MiniWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(Ui_MiniWindow, self).__init__()
        self.parentWidget = parent
        self.resize(600, 400)
        self.setStyleSheet("background-color: #333;\n"
                           "color: #00FF00;\n"
                           "font-family: Courier;")
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def DirecotriesSetup(self):
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.directoryList = QtWidgets.QListWidget(self.centralwidget)
        self.directoryList.setObjectName("directoryList")
        self.verticalLayout_2.addWidget(self.directoryList)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.removeDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.removeDirectory.setObjectName("removeDirectory")
        self.horizontalLayout.addWidget(self.removeDirectory)
        self.addDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.addDirectory.setObjectName("addDirectory")
        self.horizontalLayout.addWidget(self.addDirectory)
        self.verticalLayout.addLayout(self.horizontalLayout)
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

    def LoadHomeApps(self):
        self.resize(635, 325)
        self.appList = AllApps(self)
        self.appList.setObjectName("appList")
        self.appList.setIconSize(QtCore.QSize(75, 75))
        self.appList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.appList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.appList.setViewMode(QtWidgets.QListView.IconMode)
        self.appList.setWordWrap(True)
        self.setObjectName("homeApps")
        self.verticalLayout.addWidget(self.appList)
        self.New = QtWidgets.QPushButton(self.centralwidget)
        self.New.setObjectName("New")
        self.verticalLayout.addWidget(self.New)
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.verticalLayout.addWidget(self.deleteButton)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Apps", "Apps"))
        self.New.setText(_translate("New", "New"))
        self.deleteButton.setText(_translate("Delete", "Delete"))
        self.deleteButton.clicked.connect(self.appList.DeleteApp)
        self.deleteButton.lower()
        self.deleteButton.setEnabled(False)
        self.deleteButton.setDown(True)


        self.appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')
        apps = os.listdir(self.Apps)
        i = 0
        for app in apps:
            # get last app from json file
            appicon = self.Apps + "/" + app + "/icon/" + app
            self.app = QtWidgets.QListWidgetItem(QIcon(appicon), app)
            self.appList.insertItem(i, self.app)
            i += 1
