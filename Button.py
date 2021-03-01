from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
import UniversalVar
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from ButtonProperties import ButtonProperties

class Button(QtWidgets.QPushButton):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.parentWidget = parent
        self.move(50, 50)
        self.show()

    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        '''
        below print is very imp observation
        '''
        # print(self.text())
        self.buttonName = self.text()
        self.buttonIndex = self.parentWidget.buttonName.index(self.buttonName)

        self.menu = QtWidgets.QMenu()
        self.menu.setStyleSheet("background-color: #333;\n"
                           "color: #00FF00;\n"
                           "font-family: Courier;")

        renameAction = QAction(QIcon("icons/"), "Rename", self.menu)
        renameAction.triggered.connect(self.Rename)

        propertiesAction = QAction(QIcon("icons/"), "Properties", self.menu)
        propertiesAction.triggered.connect(self.Properties)

        removeAction = QAction(QIcon("icons/"), "Delete", self.menu)
        removeAction.triggered.connect(self.Remove)

        self.menu.addAction(renameAction)
        self.menu.addAction(propertiesAction)
        self.menu.addSeparator()
        self.menu.addSeparator()
        self.menu.addAction(removeAction)

        self.menu.popup(QtGui.QCursor.pos())

    def Remove(self):
        # self.deleteLater()
        # for json file
        self.parentWidget.buttonName.pop(self.buttonIndex)
        self.parentWidget.buttonPosition.pop(self.buttonIndex)
        self.parentWidget.buttonInterpreter.pop(self.buttonIndex)
        self.parentWidget.buttonModule.pop(self.buttonIndex)
        self.parentWidget.buttonCommand.pop(self.buttonIndex)
        self.parentWidget.terminal.append('Button Deleted : ' + self.buttonName)
        self.parentWidget.Save()

        # for run time objects
        self.parentWidget.buttonObject[self.buttonIndex].hide()
        self.parentWidget.buttonCount -= 1
        self.parentWidget.buttonObject.pop(self.buttonIndex)


    def Rename(self):
        self.parentWidget.userInput.clear()

        self.parentWidget.terminal.append('Enter new name for Button')
        self.parentWidget.userInput.setFocus(True)
        self.parentWidget.userInput.returnPressed.connect(self.RenameButton)

    def RenameButton(self):
        # this is important dissconnections, otherwise it will create multiple conections
        # in circular call between Rename and Rename Button
        self.parentWidget.userInput.disconnect()
        newname = self.parentWidget.userInput.text()

        if newname != '':

            if newname not in self.parentWidget.buttonName:

                self.parentWidget.userInput.setFocus(False)
                self.parentWidget.buttonName[self.buttonIndex] = self.parentWidget.userInput.text()
                self.parentWidget.buttonObject[self.buttonIndex].setText(self.parentWidget.userInput.text())
                self.parentWidget.terminal.append('Button Renamed to : ' + self.parentWidget.userInput.text())
                self.parentWidget.Save()

            else:
                self.parentWidget.terminal.append('button already exist')
                self.Rename()
        else:
            self.parentWidget.terminal.append('button name cannot be blank!')
            self.Rename()

    def Properties(self):

        self.properties = ButtonProperties()
        self.properties.setupUi(self.parentWidget, self.buttonName)
        self.properties.show()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            pass

    def mouseMoveEvent(self, e):

        UniversalVar.buttonIndex = self.parentWidget.buttonName.index(self.text())
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().center())

        drag.exec_(Qt.MoveAction)

    def mouseDoubleClickEvent(self, e):
        if e.button != Qt.RightButton:
            pass
        print("Double")
