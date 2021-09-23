import multiprocessing as mp

def setQueue(q, num):
    q.put(num)

def calculate(q, res):
    x = q.get()
    res.put(x**2 % 7)

if __name__ == "__main__":
    q = mp.Queue()
    res = mp.Queue()
    numbers = range(100)
    for num in numbers:
        p = mp.Process(target=setQueue, args=(q, num))
        pp = mp.Process(target=calculate, args=(q, res))
        p.start()
        pp.start()
        p.join()
        pp.join()

    while (not res.empty()):
        print("res:{}".format(res.get()))
