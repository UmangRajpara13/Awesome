from time import sleep


class Process:

    def process(self):
    	count = input()
    	print(count)
        for i in range(count):
            sleep(0.01)
            print(i)


ob = Process
ob.process(ob)
