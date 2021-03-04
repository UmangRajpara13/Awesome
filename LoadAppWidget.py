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
from TextEdit import TextEdit, PrimitiveTerminalWidget
import shutil, locale, os
from Process import Worker
import os, time
from subprocess import run, PIPE
from fbs_runtime.application_context.PyQt5 import ApplicationContext

class LoadAppWidget(QtWidgets.QMainWindow):
    # Load from JSON file
    def __init__(self, parentWidget):
        super().__init__()
        self.parentWidget = parentWidget
        self.centralwidget_2 = QtWidgets.QWidget(self)

        self.centralwidget_2.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.centralwidget_2)


        self.appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')
        self.icons = self.appctxt.get_resource('icons')
        self.Operations = self.appctxt.get_resource('operations')
        self.Iworker = Worker()
        self.InternalWorker()
        self.Eworker = Worker()
        self.ExternalWorker()
        self.Retry = False
        self.codec = locale.getpreferredencoding()

        self.LoadUi()
        self.LoadToolBarUi()

        self.buttonObject = []
        self.hideFlag = 0

        # self.AddToPath()
        # self.InitializeWorker()

    def LoadUi(self):
        self.setAcceptDrops(True)
###############
        # self.terminal = TextEdit()

        # It's good practice to put these sorts of things in constants at the top
        # rather than embedding them in your code
        DEFAULT_TTY_CMD = ['/bin/bash']
        DEFAULT_COLS = 80
        DEFAULT_ROWS = 25

        # NOTE: You can use any QColor instance, not just the predefined ones.
        DEFAULT_TTY_FONT = QtGui.QFont('Noto', 16)
        DEFAULT_TTY_FG = Qt.lightGray
        DEFAULT_TTY_BG = Qt.black

        # The character to use as a reference point when converting between pixel and
        # character cell dimensions in the presence of a non-fixed-width font
        REFERENCE_CHAR = 'W'
        self.terminal = PrimitiveTerminalWidget(self)

        # Cheap hack to estimate what 80x25 should be in pixels and resize to it
        fontMetrics = self.terminal.fontMetrics()
        # target_width = (fontMetrics.boundingRect(
        #     REFERENCE_CHAR * DEFAULT_COLS
        # ).width() + app.style().pixelMetric(QtWidgets.QStyle.PM_ScrollBarExtent))
        # self.terminal.resize(target_width, fontMetrics.height() * DEFAULT_ROWS)

        # Launch DEFAULT_TTY_CMD in the terminal
        # self.terminal.spawn(DEFAULT_TTY_CMD)


###########3
        self.verticalLayout_2.addWidget(self.terminal)

        self.buttonName = []
        self.buttonPosition = []
        self.buttonModule = []
        self.buttonInterpreter = []
        self.buttonCommand = []
        self.directoryList = []
        self.buttonCount = 0

    def AddToPath(self):
        os.environ['PATH'] = os.environ['PATH'] + ':/home/umang/Desktop/repos/Awesome/Apps/' + self.appName

    def LoadToolBarUi(self):

        self.directories = DirectoriesBox(self)
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

        # self.userInput = QtWidgets.QLineEdit()
        # self.userInput.setClearButtonEnabled(True)

        self.toolBar.addAction(addLink)
        self.toolBar.addWidget(self.directories)
        self.toolBar.addAction(addButton)
        self.toolBar.addAction(saveAction)
        self.toolBar.addAction(hideAction)
        self.toolBar.addAction(clearAction)
        self.toolBar.addAction(killProcessAction)
        # self.toolBar.addWidget(self.userInput)
        self.toolBar.addAction(terminal)

    def ExternalWorker(self):
        # self.worker = Worker()
        self.Eworker.PrintOut.connect(self.PrintOutput)
        self.Eworker.PrintError.connect(self.PrintError)
        # external
        self.Eworker.Input.connect(self.TakeInput)
        # self.Eworker.finished.connect(self.PrintUserAndHost)

    def InternalWorker(self):
        # self.worker = Worker()

        self.Iworker.PrintOut.connect(self.PrintOutput)
        self.Iworker.PrintError.connect(self.PrintError)
        # internal
        self.Iworker.takeSysInput.connect(self.TakeSysInput)
        # external
        self.Iworker.finished.connect(self.CheckForRetry)

        # self.Iworker.finished.connect(self.PrintUserAndHost)
        # self.worker.finished.connect(self.worker.deleteLater)

    def CreateNewApp(self, val):
        self.appName = val
        if not os.path.isdir(self.Apps + "/" + self.appName):
            self.directoryList.append('/home/'+getpass.getuser())
            self.directories.UpdateDirectoriesBox(self.directoryList)
            self.SaveNewApp()
        else:
            self.terminal.append('>> Already Exist! TYpe Different Name')
            self.Retry =True

    def LoadJsonData(self):
        try:

            with open(self.Apps + "/" + self.appName + "/" + self.appName + ".json", "r") as read_file:
                self.data = json.load(read_file)
                print('loaded')
        except:
            message = '''missing configuration file or error in it's format\n
                     in DIR: opt/Awesome/Apps/<app-name>/<app-name>.json,
                     visit Empower.com to obtain that config file or you can create you own!
                     and save it in above DIR and in Standard Format as described on Website!'''
            logging.error(message)
            self.terminal.append(message)

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
                    self.directoryList = data[element]

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
        self.directories.UpdateDirectoriesBox(self.directoryList)

    def NewApp(self):

        self.operation = 'newapp'
        self.message = 'Enter name for your new App:'
        self.Iworker.File_Operations_run(self.Operations, self.message)

    ## triger based

    def UpdateDirectories(self):
        self.directories.UpdateDirectoriesBox(self.directoryList)
        self.Save()

    def Terminal(self):
        os.system("gnome-terminal -e 'bash -c \"cd " + self.directories.currentText() + "; exec bash\"'")

    def AddLink(self):
        self.addLinkWindow = Ui_MiniWindow(self)
        self.addLinkWindow.DirecotriesSetup()
        self.addLinkWindow.show()

    def AddButton(self):
        # if self.Iworker.p == None:
        self.message = '>> Enter name for New Button'
        self.operation = 'newbutton'
        self.Iworker.File_Operations_run(self.Operations, self.message)

    def CreateButton(self, buttonName):

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

        else:
            self.terminal.append('>> Already exist! Type Different Name')
            self.Retry = True

    def execute(self):

        if self.Eworker.p == None:
            self.source = self.sender().text()
            self.buttonIndex = self.buttonName.index(self.source)
            self.Eworker.interpreter = self.buttonInterpreter[self.buttonIndex]
            self.Eworker.moduleName = self.buttonModule[self.buttonIndex]
            self.Eworker.command = self.buttonCommand[self.buttonIndex]
            self.Eworker.link = self.directories.currentText()

            self.Eworker.run()
        else:
            self.terminal.append('A process is running, please KILL it first!')

    def PrintOutput(self, output):
        self.terminal.setTextColor(QtGui.QColor(0,0,0,255))
        # self.terminal.setTextColor(QtGui.QColor(255,255,255,255))
        self.terminal.append(output)

    def PrintError(self, output):

        self.terminal.setTextColor(QtGui.QColor(255,192,203,255))
        self.terminal.append(output)

    def TakeInput(self):

        self.userInput.setFocus(True)
        self.userInput.returnPressed.connect(self.Read)

    def Read(self):
        #dissconnect here
        self.userInput.returnPressed.disconnect()
        self.InputValue = self.userInput.text()
        self.Eworker.WriteStdIn(self.InputValue)
        self.userInput.setFocus(False)
        self.userInput.clear()

    def TakeSysInput(self):
        self.userInput.setFocus(True)
        self.userInput.returnPressed.connect(self.ReadSysInput)

    def ReadSysInput(self):
        self.userInput.returnPressed.disconnect()
        self.InputValue = self.userInput.text()
        self.Iworker.Sys_WriteStdIn(self.InputValue)
        if self.InputValue == '':
            self.terminal.append('>> !Invalid: input feild is blank.')
            self.Retry = True
        else:
            self.terminal.append('<<< ' + self.InputValue)
            self.userInput.setFocus(False)
            self.userInput.clear()
            if self.operation == 'newapp':
                self.CreateNewApp(self.InputValue)
            if self.operation == 'newbutton':
                self.CreateButton(self.InputValue)

    def CheckForRetry(self):
        if self.Retry:
            # print('Iworker p:', self.Iworker.p)
            self.Iworker.File_Operations_run(self.Operations, self.message)
            self.Retry = False

    def KillProcess(self):

        if self.Iworker.p:
            self.terminal.setTextColor(QtGui.QColor(255, 0, 0, 255))
            self.terminal.append('--Killed--')
            self.Iworker.stop()

        if self.Eworker.p:
            self.terminal.setTextColor(QtGui.QColor(255, 0, 0, 255))
            self.terminal.append('--Killed--')
            self.Eworker.stop()


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
                    "Directories": self.directoryList

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

        # with open(self.Apps + "/" + self.appName + "/" + self.appName + ".json", "w") as write_file:
            self.data = {
                "appName" : self.appName,
                "Configuration" : {
                    "Buttons" : self.buttonName,
                    "Positions" : self.buttonPosition,
                    "Interpreters": self.buttonInterpreter,
                    "Modules": self.buttonModule,
                    "Commands": self.buttonCommand,
                    "Directories": self.directoryList
                }
            }
                # json.dump(self.data, write_file, indent=5, separators=(',', ': '))
            self.pin = '5454'
            mkdir = ['sudo', '-S', 'mkdir', self.appName]
            mkdirIcon = ['sudo', '-S', 'mkdir', 'icon']
            print(self.icons)
            copy_rename_icon = ['sudo', '-S', 'cp', self.icons + '/script.png', self.Apps + '/' + self.appName + '/icon/'+ self.appName + '.png']
            print(copy_rename_icon)
            cmd = ['sudo', '-S', 'python3', 'File_Opsave.py', str(self.Apps), str(self.appName), str(self.data)]
            try:

                logging.warning('issue may rise cause of python3 dependency')
                command = run(mkdir, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Apps)
                command = run(mkdirIcon, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Apps +'/'+ self.appName)
                command = run(copy_rename_icon, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Apps +'/'+ self.appName)
                if len(command.stdout.decode('UTF-8')) == 0:
                    print(command.stderr.decode('UTF-8'))
                else:
                    print(command.stdout.decode('UTF-8'))

                command = run(cmd, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Operations)

            except Exception as Argument:

                # creating/opening a file
                f = open(self.Operations + "/logs.txt", "a")

                # writing in the file
                f.write(str(Argument))

                # closing the file
                f.close()

            self.terminal.append('>> Created App: ' + self.appName)
        except:
            self.terminal.append('>> Could not Create App!, changes you make here won\'t be saved')


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
        # self.PrintUserAndHost()
        text = '\r'
        os.write(self.terminal.pty_m, text.encode(self.codec))

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