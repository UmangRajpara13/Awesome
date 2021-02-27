from fbs_runtime.application_context.PyQt5 import ApplicationContext
from AutomationWindow import Ui_AutomationWindow
from PyQt5 import QtCore

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Automate = Ui_AutomationWindow()
    Automate.setupUi()
    Automate.addToolBar(QtCore.Qt.BottomToolBarArea, Automate.toolBar)
    Automate.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.TopToolBarArea)
    Automate.move(650,150)
    Automate.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
