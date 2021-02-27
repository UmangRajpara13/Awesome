from time import sleep


class Process:

    def process(self):
        for i in range(1000):
            sleep(0.01)
            print(i)


ob = Process
ob.process(ob)
