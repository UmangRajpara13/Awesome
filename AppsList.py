from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import os
import shutil
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from subprocess import run, PIPE

class AllApps(QtWidgets.QListWidget):
    def __init__(self, parent):
        super(AllApps, self).__init__()
        self.parentWidget = parent
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setWordWrap(True)
        self.setObjectName("homeApps")

        self.appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
        self.Apps = self.appctxt.get_resource('Apps')

    def SetupAllApps(self):
        self.setIconSize(QtCore.QSize(75, 75))

        ##some dynamic search for apps in apps folder
        apps = os.listdir("Apps")
        i = 0
        for app in apps:
            # get last app from json file
            appicon = "Apps/" + app + "/icon/" + app
            self.app = QtWidgets.QListWidgetItem(QIcon(appicon), app)
            self.insertItem(i, self.app)
            i += 1

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        self.menu = QtWidgets.QMenu()
        # print(a0.t)
        renameAction = QAction(QIcon("icons/"), "Rename", self.menu)
        renameAction.triggered.connect(self.RenameApp)

        changeiconAction = QAction(QIcon("icons/"), "Change Icon", self.menu)
        changeiconAction.triggered.connect(self.ChangeIcon)

        deleteAction = QAction(QIcon("icons/"), "Activate Delete", self.menu)
        deleteAction.triggered.connect(self.ActivateDelete)

        self.menu.addAction(renameAction)
        self.menu.addAction(changeiconAction)
        self.menu.addSeparator()
        self.menu.addSeparator()
        self.menu.addAction(deleteAction)

        self.menu.popup(QtGui.QCursor.pos())

    def RenameApp(self):
        pass

    def ChangeIcon(self):
        pass

    def ActivateDelete(self):
        self.parentWidget.deleteButton.setEnabled(True)
        self.parentWidget.deleteButton.setDown(False)

    def DeleteApp(self):
        self.parentWidget.deleteButton.setEnabled(False)
        self.parentWidget.deleteButton.setDown(True)
        self.pin = '5454'
        cmd = ['sudo', '-S', 'rm', '-r', self.selectedItems()[0].text() ]
        try:
            # logging.warning('issue may rise cause of python3 dependency')
            command = run(cmd, stdout=PIPE, stderr=PIPE, input=self.pin.encode('UTF-8'), cwd=self.Apps)
            if len(command.stdout.decode('UTF-8')) == 0:
                print(command.stderr.decode('UTF-8'))
            else:
                print(command.stdout.decode('UTF-8'))
        except Exception as Argument:

            # creating/opening a file
            f = open(self.Operations + "/logs.txt", "a")
            # writing in the file
            f.write(str(Argument))
            # closing the file
            f.close()

        # since selectIems returns list
        self.takeItem(self.row(self.selectedItems()[0]))
        self.parentWidget.deleteButton.lower()


class AppBar(QtWidgets.QListWidget):
    def __init__(self, parent):
        super(AppBar, self).__init__()
        self.parentWidget = parent
        self.setIconSize(QtCore.QSize(50, 50))
        self.setObjectName("appBar")
        self.setViewMode(self.IconMode)
        self.setIconSize(QtCore.QSize(50, 50))
        self.setDragEnabled(False)

        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def SetupAppBarApps(self):
        pass

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        self.menu = QtWidgets.QMenu()

        closeAction = QAction(QIcon("icons/"), "Close", self.menu)
        closeAction.triggered.connect(self.CloseApp)

        self.menu.addAction(closeAction)

        self.menu.popup(QtGui.QCursor.pos())

    def CloseApp(self):
        self.parentWidget.appBar.takeItem(self.parentWidget.appBar.row(self.parentWidget.appBarObjects[self.parentWidget.stackedWidget.currentIndex()]))
        del self.parentWidget.openAppsObjects[self.parentWidget.stackedWidget.currentIndex()]
        del self.parentWidget.appBarObjects[self.parentWidget.stackedWidget.currentIndex()]

        self.parentWidget.stackedWidget.removeWidget(self.parentWidget.stackedWidget.currentWidget())
        self.parentWidget.openAppsCount -= 1
