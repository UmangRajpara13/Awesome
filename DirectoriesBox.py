from PyQt5.QtWidgets import QComboBox

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
        self.parentWidget.PrintUserAndHost()

