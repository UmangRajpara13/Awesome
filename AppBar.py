from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import os
import shutil
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from subprocess import run, PIPE

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
