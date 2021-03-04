from fbs_runtime.application_context.PyQt5 import ApplicationContext
from AutomationWindow import AutomationWindow
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
import sys

import sys

if __name__ == '__main__':
    # appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    app.setStyle('Fusion')
    Automate = AutomationWindow()
    Automate.setupUi()
    Automate.addToolBar(QtCore.Qt.BottomToolBarArea, Automate.toolBar)
    Automate.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea| QtCore.Qt.TopToolBarArea)
    Automate.move(650,150)
    Automate.show()

    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)
    app.exec_()