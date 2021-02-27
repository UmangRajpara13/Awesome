from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5 import Qt, QtGui

class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("terminal")
        self.setReadOnly(True)
