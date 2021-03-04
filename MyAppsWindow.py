from PyQt5 import QtCore
from PyQt5 import QtWidgets
import os
from PyQt5.QtGui import QIcon
from AppsList import AllApps
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import getpass, json
from subprocess import run, PIPE

class MyAppsWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MyAppsWindow, self).__init__()
        #writing parent above is taking theme of parent
        # self.parent = parent
        self.setObjectName("MyAppsWindow")

        self.appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')
        self.icons = self.appctxt.get_resource('icons')
        self.Operations = self.appctxt.get_resource('operations')
        self.resize(600, 400)
        # self.setStyleSheet("background-color: #333;\n"
        #                    "color: #00FF00;\n"
        #                    "font-family: Courier;")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.label = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.appList.DeleteApp)
        self.deleteButton.lower()
        self.deleteButton.setEnabled(False)
        self.deleteButton.setDown(True)
        self.horizontalLayout.addWidget(self.deleteButton)

        self.New = QtWidgets.QPushButton(self.centralwidget)
        self.New.setObjectName("New")
        self.New.clicked.connect(self.NewApp)
        self.horizontalLayout.addWidget(self.New)

        self.lineEdit = None

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("My Apps", "My Apps"))
        self.New.setText(_translate("New", "New"))
        self.deleteButton.setText(_translate("Delete", "Delete"))
        QtCore.QMetaObject.connectSlotsByName(self)


    def LoadHomeApps(self):

        apps = os.listdir(self.Apps)
        i = 0
        for app in apps:
            # get last app from json file
            appicon = self.Apps + "/" + app + "/icon/" + app
            self.app = QtWidgets.QListWidgetItem(QIcon(appicon), app)
            self.appList.insertItem(i, self.app)
            i += 1

    def NewApp(self):
        if self.lineEdit == None:
            self.lineEdit = QtWidgets.QLineEdit()
            self.label.setText('Enter Name for you App!')
            self.lineEdit.returnPressed.connect(self.CreateNewApp)
            self.horizontalLayout.addWidget(self.lineEdit)
        else:
            self.lineEdit.show()

    def CreateNewApp(self):
        self.newAppName = self.lineEdit.text()
        self.lineEdit.hide()
        self.lineEdit.clear()

### only for linux

        if not os.path.isdir('/home/' + getpass.getuser() + "/" + 'Awesome_User' + "/" + self.newAppName):
            self.label.setText('Creating')
            self.SaveNewApp()
            # self.directoriesBox.UpdateDirectoriesBox(self.directoryList)
        else:
            self.label.setText('>> Already Exist! TYpe Different Name')
            # self.Retry = True

    def SaveNewApp(self):
        self.buttonName = []
        self.buttonPosition = []
        self.buttonModule = []
        self.buttonInterpreter = []
        self.buttonCommand = []
        self.directoryList = []
        self.directoryList.append('/home/' + getpass.getuser())

        self.pin = '5454'

        mkdir = ['sudo', '-S', 'mkdir', self.newAppName]
        try:
            command = run(mkdir, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd='/home/' + getpass.getuser() + '/Awesome_User')

            try:
                self.data = {
                    "appName": self.newAppName,
                    "Configuration": {
                        "Buttons": self.buttonName,
                        "Positions": self.buttonPosition,
                        "Interpreters": self.buttonInterpreter,
                        "Modules": self.buttonModule,
                        "Commands": self.buttonCommand,
                        "Directories": self.directoryList
                    }
                }
                cmd = ['sudo', '-S', 'python3', 'File_Opsave.py',
                       '/home/' + getpass.getuser() + '/Awesome_User', str(self.newAppName), str(self.data)]

                command = run(cmd, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'),
                              cwd=self.Operations)
                self.label.setText('>> Created App: ' + self.newAppName)

            except:
                self.label.setText('>> Could not Create App Configuration!')

            mkdirIcon = ['sudo', '-S', 'mkdir', 'icon']

            try:
                command = run(mkdirIcon, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'),
                              cwd='/home/' + getpass.getuser() + '/Awesome_User/' + self.newAppName)

                copy_rename_icon = ['sudo', '-S', 'cp', self.icons + '/script.png',
                                    '/home/' + getpass.getuser() + '/Awesome_User/' + self.newAppName + '/icon/' + self.newAppName + '.png']
                try:
                    command = run(copy_rename_icon, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'),
                                  cwd='/home/' + getpass.getuser() + '/Awesome_User/' + 'icon')

                except:
                    self.label.setText('could not copy icon')

            except:
                self.label.setText('could not create Icon dir')

        except:
            self.label.setText('Failed')
