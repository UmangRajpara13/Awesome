from multiprocessing import Process, Queue
from time import sleep
# def f(q):
#     q.put([42, None, 'hello'])
#     sleep(5)
#
# if __name__ == '__main__':
#     q = Queue()
#     p = Process(target=f, args=(q,))
#     p.start()
#     # prints "[42, None, 'hello']"
#     # p.join()
#     print(q.get())


def func(q):
    # cannot send out messa like above coz of multipr

    # self.takeSysInput.emit()
    inp = q.get()
    print(q.empty())

    print(inp)
    # after get queue is empty
    if inp != '' and inp != '0':
        print(q.empty())
        q.put('msg command')
        print(q.empty())
        # raise some signal
    else:
        func(q)