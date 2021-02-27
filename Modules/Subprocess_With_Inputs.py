import subprocess
import sys

class Process:


    def process_with_inputs(self):

        self.command = sys.argv[1]
        self.link = sys.argv[2]

        print('Enter Commit Message')
        print('->')
        self.message = input()

        self.command = self.command.split()
        self.command.append(self.message)
        print(self.command)

        command = subprocess.run(self.command, cwd=self.link, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        if len(command.stdout.decode('UTF-8')) == 0:
            print(command.stderr.decode('UTF-8'))
        else:
            print(command.stdout.decode('UTF-8'))


ob = Process
ob.process_with_inputs(ob)