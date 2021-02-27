from PyQt5.QtWidgets import QComboBox
from PyQt5 import QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import UniversalVar
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from ButtonProperties import ButtonProperties

class DirectoriesBox(QComboBox):

    def __init__(self, parentWidget):
        super(DirectoriesBox, self).__init__()
        self.parentWidget = parentWidget
        self.setFrame(True)
        self.setObjectName("DirectoriesBox")
        self.currentIndexChanged.connect(self.DirectoryBoxChanged)


    # def contextMenuEvent(self, e: QtGui.QContextMenuEvent) -> None:
    #
    #     self.menu = QtWidgets.QMenu()
    #
    #     removeAction = QAction(QIcon("icons/"), "Remove", self.menu)
    #     removeAction.triggered.connect(self.RemoveLink)
    #
    #     self.menu.addAction(removeAction)
    #     self.menu.popup(QtGui.QCursor.pos())

    # def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
    #     # if e.button != Qt.RightButton:
    #     self.showPopup()

    def UpdateDirectoriesBox(self, directory):
        self.clear()
        for i in range(len(directory)):
            self.addItem(directory[i])

    def DirectoryBoxChanged(self):
        self.parentWidget.PrintUserAndHost()

