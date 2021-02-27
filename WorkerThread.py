
from PyQt5.QtCore import QObject, pyqtSignal, QProcess


class Worker(QObject):
    finished = pyqtSignal()
    started = pyqtSignal()
    Input = pyqtSignal()
    PrintOut = pyqtSignal(str)
    PrintError = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.p = None

    def run(self):
        if not self.p:
            self.started.emit()
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            # self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)
            if self.interpreter.find('python') != -1:
                self.p.setWorkingDirectory('./Modules')

            if self.interpreter.find('/bin/sh') != -1:
                self.p.setWorkingDirectory('/home/umang/.local/bin')

            self.p.start(self.interpreter, [self.moduleName, self.command, self.link])


    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.PrintError.emit(stderr)

    def handle_stdout(self):

        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.PrintOut.emit(stdout)
        if stdout.find('->') != -1:
            self.Input.emit()

    def process_finished(self):
        self.finished.emit()
        self.p = None

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.PrintOut.emit(f"State changed: {state_name}")

    def WriteStdIn(self, stdinput):
        stdinput = stdinput + '\n'
        stdinput = bytes(stdinput.encode('UTF-8'))
        self.p.write(stdinput)


    def stop(self):

        self.p.kill()
        # self.finished.emit()
        self.p = None
