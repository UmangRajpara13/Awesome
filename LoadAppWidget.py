from PyQt5 import QtWidgets, QtCore, QtGui
from Button import Button
from MiniWindow import Ui_MiniWindow
from PyQt5.QtCore import Qt
import json, logging
import getpass, socket
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from DirectoriesBox import DirectoriesBox
import UniversalVar
from TextEdit import TextEdit
import shutil
from Process import Worker
import os
from subprocess import run, PIPE
from fbs_runtime.application_context.PyQt5 import ApplicationContext

class LoadAppWidget(QtWidgets.QMainWindow):
    # Load from JSON file
    def __init__(self, parentWidget):
        super().__init__()
        self.parentWidget = parentWidget
        self.appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')
        self.icons = self.appctxt.get_resource('icons')
        self.Operations = self.appctxt.get_resource('operations')

        self.worker = Worker()
        self.worker.PrintOut.connect(self.PrintOutput)
        self.worker.PrintError.connect(self.PrintError)

#internal
        # self.worker.PrintOut.connect(self.HandleSysOutput)
        self.worker.Input.connect(self.TakeSysInput)
        # self.worker.finished.connect(self.)
#external
        self.worker.Input.connect(self.TakeInput)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.worker.finished.connect(self.worker.deleteLater)


        self.LoadUi()
        # self.AddToPath()
        self.LoadToolBarUi()

        if parentWidget.appNameText != "New":
            self.appName = parentWidget.appNameText
            try:
                with open(self.Apps + "/" + self.appName + "/" + self.appName + ".json", "r") as read_file:
                    self.data = json.load(read_file)
            except:
                message = '''missing configuration file or error in it's format\n
                         in DIR: opt/Awesome/Apps/<app-name>/<app-name>.json,
                         visit Empower.com to obtain that config file or you can create you own!
                         and save it in above DIR and in Standard Format as described on Website!'''
                logging.error(message)
                self.terminal.append(message)
        else:
            # self.PrintUserAndHost()
            #
            # self.directory.append('/home')
            # self.directories.UpdateDirectoriesBox(self.directory)
            self.operation = 'newapp'

            self.message = 'Enter name for your new App:'
            self.worker.File_Operations_run(self.Operations, self.message)



        self.buttonObject = []
        self.hideFlag = 0

    def CreateNewApp(self, val):
        self.appName = val
        if not os.path.isdir(self.Apps + "/" + self.appName):
            self.directory.append('/home/'+getpass.getuser())
            self.directories.UpdateDirectoriesBox(self.directory)
            self.SaveNewApp()

            # self.worker.p.kill()
            # self.worker.p = None
        else:
            self.terminal.append('choose another Name')
            # self.worker.p.kill()
            # self.worker.p = None
            self.worker.File_Operations_run(self.Operations, self.message)
        # self.BeginProcess(self.operation)


    # def BeginProcess(self, operation):
    #     if self.IP == None:
    #         self.IP = 'something'
    #         self.terminal.append('--process begin--')
    #         if operation == 'newapp':
    #             self.msg = 'Enter name for your new App:'
    #         if operation == 'newbutton':
    #             self.msg = 'Enter name for New Button'
    #         self.TakeSysInput()
    #     else:
    #         self.terminal.append('A process is running, please KILL it first!')

    # def ContinueProcess(self):
    #     if self.InputValue != '0':
    #         if self.operation == 'newapp':
    #             pass
    #         if self.operation == 'newbutton':
    #             buttonName = self.InputValue
    #             if buttonName in self.buttonName:
    #                 self.terminal.append('Already Exist! Type different name!')
    #                 self.TakeSysInput()
    #             else:
    #                 self.CreateButton(buttonName)

        self.InputValue = '0'

    def LoadUi(self):
        self.setAcceptDrops(True)
        self.dockWidget = QtWidgets.QDockWidget(self)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.terminal = TextEdit()
        self.verticalLayout_2.addWidget(self.terminal)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)
        self.buttonName = []
        self.buttonPosition = []
        self.buttonModule = []
        self.buttonInterpreter = []
        self.buttonCommand = []
        self.directory = []
        self.InputValue = '0'


        self.buttonCount = 0

    def AddToPath(self):
        os.environ['PATH'] = os.environ['PATH'] + ':/home/umang/Desktop/repos/Awesome/Apps/' + self.appName

    def LoadToolBarUi(self):

        self.directories = DirectoriesBox(self)
        # self.AddDirectory = QtWidgets.QToolButton

        self.toolBar = QtWidgets.QToolBar(self.parentWidget.stackedWidget.currentWidget())
        self.toolBar.setStyleSheet("height : 50px;")
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setFixedHeight(40)
        self.toolBar.setIconSize(QtCore.QSize(40, 40))
        self.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.toolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)

        addLink = QAction(QIcon(self.icons + "/edit"), "Ctrl+B", self)
        addLink.setShortcut("Ctrl+B")
        addLink.triggered.connect(self.AddLink)

        addButton = QAction(QIcon(self.icons + "/newbutton"), "Alt+B", self)
        addButton.setShortcut("Alt+B")
        addButton.triggered.connect(self.AddButton)

        saveAction = QAction(QIcon(self.icons + "/save"), "Ctrl+S", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.Save)

        hideAction = QAction(QIcon(self.icons + "/hide"), "Ctrl+Q", self)
        hideAction.setShortcut("Alt+Q")
        hideAction.triggered.connect(self.Hide)

        killProcessAction = QAction(QIcon(self.icons + "/kill"), "Ctrl+Z", self)
        killProcessAction.setShortcut("Ctrl+Z")
        killProcessAction.triggered.connect(self.KillProcess)

        clearAction = QAction(QIcon(self.icons + "/clear"), "Alt+Z", self)
        clearAction.setShortcut("Alt+Z")
        clearAction.triggered.connect(self.Clear)

        terminal = QAction(QIcon(self.icons + "/terminal"), "Alt+.", self)
        terminal.setShortcut("Alt+.")
        terminal.triggered.connect(self.Terminal)

        self.userInput = QtWidgets.QLineEdit()
        self.userInput.setClearButtonEnabled(True)

        self.toolBar.addAction(addLink)
        self.toolBar.addWidget(self.directories)
        self.toolBar.addAction(addButton)
        self.toolBar.addAction(saveAction)
        self.toolBar.addAction(hideAction)
        self.toolBar.addAction(clearAction)
        self.toolBar.addAction(killProcessAction)
        self.toolBar.addWidget(self.userInput)
        self.toolBar.addAction(terminal)



    def DeSerializeJson(self, data):

        for element in data: #data is dict
            if (isinstance(data[element], str)):    # first element is string
                if element == "appName":
                    self.appName = data[element]
            if (isinstance(data[element], dict)):   # second element is dict
                self.DeSerializeJson(data[element])
            if (isinstance(data[element], list)):
                if element == "Buttons":
                    self.buttonName = data[element]
                if element == "Positions":
                    self.buttonPosition = data[element]
                if element == "Interpreters":
                    self.buttonInterpreter = data[element]
                if element == "Modules":
                    self.buttonModule = data[element]
                if element == "Commands":
                    self.buttonCommand = data[element]
                if element == "Directories":
                    self.directory = data[element]


    def CreateAttributes(self):
        #Buttons
        for i in range(len(self.buttonName)):
            self.buttonObject.append(None)
            self.buttonObject[self.buttonCount] = Button(self.buttonName[i], self.parentWidget.stackedWidget.currentWidget())
            self.buttonObject[self.buttonCount].setMouseTracking(True)
            self.buttonObject[self.buttonCount].clicked.connect(self.execute)
            self.location = self.buttonPosition[i].split(",")
            self.buttonObject[self.buttonCount].move(float(self.location[0]),float(self.location[1]))
            self.buttonCount += 1
        #Directories
        self.directories.UpdateDirectoriesBox(self.directory)

## triger based

    def UpdateDirectories(self):
        self.directories.UpdateDirectoriesBox(self.directory)
        self.Save()

    def Terminal(self):
        os.system("gnome-terminal -e 'bash -c \"cd " + self.directories.currentText() + "; exec bash\"'")

    def AddLink(self):
        self.addLinkWindow = Ui_MiniWindow(self)
        self.addLinkWindow.DirecotriesSetup()
        self.addLinkWindow.show()

    def AddButton(self):
        if self.worker.p == None:
            self.message = 'Enter name for New Button'
            self.operation = 'newbutton'
            self.worker.File_Operations_run(self.Operations, self.message)

    def CreateButton(self, buttonName):
        # self.userInput.setFocus(False)
        # self.userInput.disconnect()
        if buttonName not in self.buttonName:
            self.buttonName.append(buttonName)
            self.buttonPosition.append("50,50")
            self.buttonObject.append(None)
            self.buttonObject[self.buttonCount] = Button(buttonName, self.parentWidget.stackedWidget.currentWidget())
            self.buttonObject[self.buttonCount].setMouseTracking(True)
            self.buttonObject[self.buttonCount].clicked.connect(self.execute)
            self.terminal.append('Added New Button : ' + self.userInput.text())
            self.buttonInterpreter.append("python3")
            self.buttonModule.append("Subprocess.py")
            self.buttonCommand.append("echo hello")
            self.buttonCount += 1
            self.Save()
            # self.worker.p.kill()
            # self.worker.p = None
        else:
            self.terminal.append('Already exist!')
            # self.worker.p.kill()
            # self.worker.p = None
            self.worker.File_Operations_run(self.Operations, self.message)


    # def InternalOps(self):
    #     if self.worker.p == None:
    #         # self.worker = Worker()
    #
    #         self.WorkerProcess()
    #     else:
    #         self.terminal.append('A process is running, please KILL it first!')


    def execute(self):

        if self.worker.p == None:
            # self.worker = Worker()
            self.source = self.sender().text()
            self.buttonIndex = self.buttonName.index(self.source)
            self.worker.interpreter = self.buttonInterpreter[self.buttonIndex]
            self.worker.moduleName = self.buttonModule[self.buttonIndex]
            self.worker.command = self.buttonCommand[self.buttonIndex]
            self.worker.link = self.directories.currentText()

            self.WorkerProcess()
        else:
            self.terminal.append('A process is running, please KILL it first!')


    def WorkerProcess(self):

        self.worker.finished.connect(self.PrintUserAndHost)
        self.worker.run()


    def PrintOutput(self, output):
        self.terminal.setTextColor(QtGui.QColor(0,0,0,255))

        # self.terminal.setTextColor(QtGui.QColor(255,255,255,255))
        self.terminal.append(output)

    def PrintError(self, output):

        self.terminal.setTextColor(QtGui.QColor(255,192,203,255))
        self.terminal.append(output)

    def TakeInput(self):

        self.userInput.setFocus(True)
        self.userInput.returnPressed.connect(self.read)

    def read(self):
        #dissconnect here
        print('reading input')

        self.userInput.returnPressed.disconnect()
        self.InputValue = self.userInput.text()
        self.worker.WriteStdIn(self.InputValue)
        self.userInput.setFocus(False)
        self.userInput.clear()

    # def HandleSysOutput(self, output):
    #     if output == '':
    #         self.terminal.append('Invalid Input:',output)
    #         self.KillProcess()
    #         self.worker.File_Operations_run(self.Operations, self.message)
    #     else:
    #         self.terminal.append('ok')

    def TakeSysInput(self):
        self.userInput.setFocus(True)
        self.userInput.returnPressed.connect(self.ReadSysInput)

    def ReadSysInput(self):
        self.userInput.returnPressed.disconnect()
        self.InputValue = self.userInput.text()
        self.worker.WriteStdIn(self.InputValue)
        if self.InputValue == '':
            self.terminal.append('!Invalid: input feild is blank.')
            # self.KillProcess()
            # self.worker.p.kill()
            # self.worker.p = None
            self.worker.File_Operations_run(self.Operations, self.message)
        else:
            self.userInput.setFocus(False)
            self.userInput.clear()
            self.terminal.append('ok')
            if self.operation == 'newapp':
                self.CreateNewApp(self.InputValue)
            if self.operation == 'newbutton':
                self.CreateButton(self.InputValue)
            # self.ContinueProcess()

    def KillProcess(self):

        if self.worker.p:
            self.terminal.setTextColor(QtGui.QColor(255, 0, 0, 255))
            self.terminal.append('--Killed--')
            self.worker.stop()


    def PrintUserAndHost(self):
        self.terminal.setTextColor(QtGui.QColor(255, 140, 0, 255))
        self.terminal.append(getpass.getuser() + '@' + socket.gethostname() + ' : ' + self.directories.currentText())

    def Save(self):
        if self.parentWidget.openAppsObjects[self.parentWidget.stackedWidget.currentIndex()].appName == "New":
            self.newapp = Ui_MiniWindow()
            self.newapp.SaveAppSetup()
            self.newapp.lineEdit.returnPressed.connect(self.SaveNewApp)
            self.newapp.show()

        else:
            self.data = {
                "appName" : self.appName,
                "Configuration" : {
                    "Buttons" : self.buttonName,
                    "Positions" : self.buttonPosition,
                    "Interpreters": self.buttonInterpreter,
                    "Modules": self.buttonModule,
                    "Commands": self.buttonCommand,
                    "Directories": self.directory

                }
            }

            # os.environ['SUDO_ASKPASS'] = '/usr/bin/ssh-askpass'

            self.pin = '5454'

            cmd = ['sudo', '-S', 'python3', 'File_Opsave.py', str(self.Apps), str(self.appName), str(self.data)]

            try:

                logging.warning('issue may rise cause of python3 dependency')
                command = run(cmd, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Operations)

            except Exception as Argument:

                # creating/opening a file
                f = open(self.Operations + "/logs.txt", "a")

                # writing in the file
                f.write(str(Argument))

                # closing the file
                f.close()

    def SaveNewApp(self):

        try:
            path = self.Apps + "/" + self.appName
            os.mkdir(path)
            with open(self.Apps + "/" + self.appName + "/" + self.appName + ".json", "w") as write_file:
                self.data = {
                    "appName" : self.appName,
                    "Configuration" : {
                        "Buttons" : self.buttonName,
                        "Positions" : self.buttonPosition,
                        "Interpreters": self.buttonInterpreter,
                        "Modules": self.buttonModule,
                        "Commands": self.buttonCommand,
                        "Directories": self.directory
                    }
                }
                json.dump(self.data, write_file, indent=5, separators=(',', ': '))
            path = self.Apps + "/" + self.appName + "/icon"
            os.mkdir(path)
            shutil.copy2(self.icons + "/script.png", path)
            os.rename( path + '/script.png', path + '/' + self.appName +'.png')
            self.terminal.append('Success, Created' + self.appName)
        except:
            self.terminal.append('Could not Create App!, changes you make here wont be saved')


    def Hide(self):
        if self.hideFlag == 0:
            for i in range(len(self.buttonObject)):
                    self.buttonObject[i].hide()
            self.hideFlag = 1
        else:
            for i in range(len(self.buttonObject)):
                self.buttonObject[i].show()
            self.hideFlag = 0

    def Clear(self):
        self.terminal.clear()
        self.PrintUserAndHost()

    def dragEnterEvent(self, e):
        e.accept()
        self.buttonObject[UniversalVar.buttonIndex].move(e.pos())

    def dragMoveEvent(self, e):
        e.accept()
        self.buttonObject[UniversalVar.buttonIndex].move(e.pos())

    def dropEvent(self, e):
        self.buttonObject[UniversalVar.buttonIndex].move(e.pos())
        self.buttonObject[UniversalVar.buttonIndex].setDown(False)
        self.buttonPosition[UniversalVar.buttonIndex] = str(e.posF().x()) + "," + str(e.posF().y())
        e.setDropAction(Qt.MoveAction)
        e.ignore()
        self.Save()