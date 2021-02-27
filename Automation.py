from AutomationWindow import Ui_AutomationWindow
import sys
from PyQt5 import QtWidgets, QtCore


app = QtWidgets.QApplication(sys.argv)
Automate = Ui_AutomationWindow()
Automate.setupUi()
Automate.addToolBar(QtCore.Qt.BottomToolBarArea, Automate.toolBar)
Automate.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.TopToolBarArea)
Automate.move(650,150)
Automate.show()

app.exec_()
