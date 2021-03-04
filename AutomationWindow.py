from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from AppBar import AppBar
from LoadAppWidget import LoadAppWidget
from MyAppsWindow import MyAppsWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import UniversalVar
from Settings import Settings

class AutomationWindow(QtWidgets.QMainWindow):
    def setupUi(self):

        #Developer defined
        self.openAppsObjects = []
        self.appBarObjects = []
        self.openAppsCount = 0
        self.appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')
        self.icons = self.appctxt.get_resource('icons')
        self.desktop = QtWidgets.QDesktopWidget()
        UniversalVar.width = self.desktop.width()
        UniversalVar.height = self.desktop.height()
        #reimplemented
        self.resize(700, 500)
        self.setObjectName("AutomationWindow")

        # this is master style sheet affecting all child widgets
        self.setStyleSheet("background-color: #466460;\n"
                           "color: #FFFFFF;\n"
                            "font-family: Courier;")
        # self.setStyleSheet("background-color: #59360a;\n"
        #                    "color: #000000;\n"
        #                    "font-family: Courier;")
#         self.setWindowOpacity(0.8)


        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.verticalLayout.addWidget(self.stackedWidget)
        self.LoadAppBarUi()
        self.LoadToolBarUi()
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Awesome", "Awesome"))
        # self.homeApps.setSortingEnabled(True)


    def RefreashHomeApps(self):
        self.homeApps.clear()
        self.homeApps.SetupAllApps()
        self.homeApps.itemPressed.connect(self.openApp)

    def LoadAppBarUi(self):
        self.appBar = AppBar(self)
        self.appBar.SetupAppBarApps()
        self.appBar.itemPressed.connect(self.switch)

    def LoadToolBarUi(self):

        self.toolBar = QtWidgets.QToolBar(self)
        # self.toolBar.setStyleSheet("height : 15000px;")
        self.toolBar.setObjectName("toolBar")
        # 10% height
        self.toolBar.setFixedHeight(UniversalVar.height/10)
        self.toolBar.setIconSize(QtCore.QSize(UniversalVar.height/20, UniversalVar.height/20))

        openAction = QAction(QIcon(self.icons + "/open"), "Ctrl+N", self)
        openAction.setShortcut("Ctrl+N")
        openAction.setStatusTip("Open")
        openAction.triggered.connect(self.Open)

        settingsAction = QAction(QIcon(self.icons + "/settings"), "Ctrl+M", self)
        settingsAction.setShortcut("Ctrl+M")
        settingsAction.triggered.connect(self.Settings)

        infoAction = QAction(QIcon(self.icons + "/info"), "Alt+i", self)
        infoAction.setShortcut("Alt+X")
        infoAction.triggered.connect(self.Info)

        self.toolBar.addAction(openAction)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.appBar)
        self.toolBar.addSeparator()
        self.toolBar.addAction(infoAction)
        self.toolBar.addAction(settingsAction)

    ###trigger based

    def Open(self):
            self.home = MyAppsWindow()
            self.home.LoadHomeApps()
            self.home.appList.itemDoubleClicked.connect(self.openApp)
            self.home.appList.itemPressed.connect(self.getItemName)
            self.home.move(0, UniversalVar.height*0.425)
            self.home.show()

    def openApp(self, item):
        self.home.close()

        if (self.appBar.findItems(str(item.text()), QtCore.Qt.MatchFlag.MatchExactly) == []):
            self.openAppsObjects.append(None)
            self.openAppsObjects[self.openAppsCount] = LoadAppWidget(self)
            self.openAppsObjects[self.openAppsCount].appName = item.text()
            self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.openAppsObjects[self.openAppsCount]))
            self.openAppsObjects[self.openAppsCount].LoadJsonData()
            self.openAppsObjects[self.openAppsCount].DeSerializeJson(self.openAppsObjects[self.openAppsCount].data)
            self.openAppsObjects[self.openAppsCount].CreateAttributes()

            app = self.openAppsObjects[self.stackedWidget.currentIndex()].appName
            appicon = self.Apps + "/" + app + "/icon/" + app
            self.appBarObjects.append(None)
            self.appBarObjects[self.openAppsCount] = QtWidgets.QListWidgetItem(QIcon(appicon), app)
            self.appBar.insertItem(self.stackedWidget.currentIndex(), self.appBarObjects[self.openAppsCount])
            self.appBar.setCurrentRow(self.openAppsCount)
            self.openAppsCount += 1

    def OpenNewApp(self):
        self.home.close()
        self.openAppsObjects.append(None)
        self.openAppsObjects[self.openAppsCount] = LoadAppWidget(self)
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.openAppsObjects[self.openAppsCount]))

        self.openAppsObjects[self.stackedWidget.currentIndex()].appName = "New"
        self.openAppsObjects[self.stackedWidget.currentIndex()].NewApp()

        app = self.openAppsObjects[self.stackedWidget.currentIndex()].appName
        appicon = self.icons + '/new.png'
        self.appBarObjects.append(None)
        self.appBarObjects[self.openAppsCount] = QtWidgets.QListWidgetItem(QIcon(appicon), app)
        self.appBar.insertItem(self.stackedWidget.currentIndex(), self.appBarObjects[self.openAppsCount])
        self.appBar.setCurrentRow(self.openAppsCount)
        self.openAppsCount += 1


    def getItemName(self, item):
        UniversalVar.itemName = item.text()
        print(UniversalVar.itemName)

    def Settings(self):
        self.settings = Settings(self)
        self.settings.show()

    def switch(self, item):
        self.stackedWidget.setCurrentIndex(self.appBar.row(item))

    def Info(self):
        pass
