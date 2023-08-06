pythonGroupMsg Queue multicast broadcast
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

cython  Broadcasting to multiple queues
========================================

 Recently, I'm going to do something like chat software. After a lot of testing, I've done this thing.

    Performance is 13 times faster than py direct circular transmission


install ::

    pip install pythonGroupMsg

push msg
++++++++

python ::

    from lib.threadTimeWheel import TimeLoop
    import random
    t = TimeLoop()
    t.start()
    r = random.Random()

    import time
    def hello():
        print("test",time.asctime())

    if __name__ == '__main__':
        for i in range(1,10000):
            t.insertTask(hello,r.randint(1,100))
            print(t.getAllTaskSize())
            print(t.getOldTaskSize())










