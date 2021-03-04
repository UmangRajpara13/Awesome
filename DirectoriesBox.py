from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont, QPalette, QTextCursor  # type: ignore


class DirectoriesBox(QComboBox):

    def __init__(self, parentWidget):
        super(DirectoriesBox, self).__init__()
        self.parentWidget = parentWidget
        self.setFrame(True)
        self.setObjectName("DirectoriesBox")
        self.currentIndexChanged.connect(self.DirectoryBoxChanged)

    def UpdateDirectoriesBox(self, directory):
        self.clear()
        for i in range(len(directory)):
            self.addItem(directory[i])

    def DirectoryBoxChanged(self):
        self.parentWidget.terminal.moveCursor(QTextCursor.End)
        # text= ('cd ' + self.currentText()).encode('UTF-8')
        # print(text)
        import locale, os
        self.codec = locale.getpreferredencoding()
        text = 'cd ' + self.currentText() + '\r'
        # self.parentWidget.terminal.insertPlainText('cd ' + self.currentText())
        os.write(self.parentWidget.terminal.pty_m, text.encode(self.codec))

        print(self.parentWidget.terminal.backspace_budget)
        # self.parentWidget.terminal.cursor.insertText('\r')
        # pass
        # self.parentWidget.terminal.append('cd ' + self.currentText() + '\x13')
        # self.parentWidget.PrintUserAndHost()

