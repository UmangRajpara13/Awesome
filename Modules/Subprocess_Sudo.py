import subprocess
import sys

class ProcessSudo:

    def process_with_sudo(self):

        self.command = sys.argv[1]
        self.link = sys.argv[2]
        # self.PIN = sys.argv[3]

        print('Enter PIN')
        print('->')
        self.PIN = input()

        command = subprocess.run(self.command, input=self.PIN.encode('UTF-8'), shell=True, cwd=self.link, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        if len(command.stdout.decode('UTF-8')) == 0:
            print(command.stderr.decode('UTF-8'))
        else:
            print(command.stdout.decode('UTF-8'))


ob = ProcessSudo
ob.process_with_sudo(ob)
