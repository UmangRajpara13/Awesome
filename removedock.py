# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'removedock.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setObjectName("self")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtWidgets.QMainWindow()
        self.page.setObjectName("page")
        self.centralwidget_2 = QtWidgets.QWidget(self.page)

        self.centralwidget_2.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.toolBar_2 = QtWidgets.QToolBar(self.page)
        self.toolBar_2.setStyleSheet("height : 50px;")
        self.toolBar_2.setObjectName("toolBar_2")
        self.toolBar_2.setFixedHeight(40)
        self.toolBar_2.setIconSize(QtCore.QSize(40, 40))
        self.toolBar_2.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.toolBar_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.page.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar_2)

        self.page.setCentralWidget(self.centralwidget_2)

        self.textEdit = QtWidgets.QTextEdit(self.page)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtWidgets.QMainWindow()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.toolBar = QtWidgets.QToolBar(self.stackedWidget.currentWidget())
        self.toolBar.setStyleSheet("height : 50px;")
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setFixedHeight(40)
        self.toolBar.setIconSize(QtCore.QSize(40, 40))
        self.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea | QtCore.Qt.TopToolBarArea)
        self.toolBar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)
        self.stackedWidget.setCurrentWidget(self.page)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    app.setStyle('Fusion')

    # appctxt = ApplicationContext()
    # Apps = appctxt.get_resource('Apps')
    # print(Apps)
    Automate = Ui_MainWindow()
    # Automate.setupUi()
    # Automate.addToolBar(QtCore.Qt.BottomToolBarArea, Automate.toolBar)
    # Automate.toolBar.setAllowedAreas(QtCore.Qt.BottomToolBarArea|QtCore.Qt.TopToolBarArea)
    # Automate.move(650,150)
    Automate.show()


    # app.exec_()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)
    app.exec_()