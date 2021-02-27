import sys
import subprocess
import os
import threading

class Process:

	def process(self):
		# sys.argv[1] is command
		# sys.argv[2] is directory
		self.command = sys.argv[1]
		self.link = sys.argv[2]

		command = subprocess.run(self.command, shell=True, cwd=self.link, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		if len(command.stdout.decode('UTF-8')) == 0:
			print(command.stderr.decode('UTF-8'))
		else:
			print(command.stdout.decode('UTF-8'))


ob = Process()
ob.process()
