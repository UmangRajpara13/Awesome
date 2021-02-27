import subprocess
import sys

class ProcessCall:


	def process(self):

		self.command = sys.argv[1]
		self.link = sys.argv[2]

		command = subprocess.run(self.command, shell=True, cwd=self.link)

		if len(command.stdout.decode('UTF-8')) == 0:
			print(command.stderr.decode('UTF-8'))
		else:
			print(command.stdout.decode('UTF-8'))

ob = ProcessCall
ob.process(ob)