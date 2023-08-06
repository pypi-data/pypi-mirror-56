import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor

class TimeLoop(threading.Thread):
    __oninit = int(time.time())
    __probe = 0
    __loop = {}
    __max = 10
    __task = 0
    __old = 0
    __errors = []
    __pool = None
    __isPool = True
    def run(self):
        while True:
            if self.__probe > self.__max:
                self.__probe = 0
                self.__oninit = int(time.time())
            self.__probe  = int(time.time()) - self.__oninit
            if self.__probe in self.__loop:
                if len(self.__loop[self.__probe]) > 0:
                    for i in self.__loop[self.__probe]:
                        try:
                            if self.__isPool:
                                self.__pool.submit(i)
                            else:
                                i()
                        except Exception as e:
                            self.__errors.append(str(e))
                        finally:
                            self.__task-=1
                            self.__old +=1

                    self.__loop[self.__probe] = []
            if len(self.__errors) > 0:
                print(self.__errors.pop())
    def start(self,isPool=True,size = 3):
        self.__isPool = isPool
        if self.__isPool:
            self.__pool = ThreadPoolExecutor(thread_name_prefix="TimeWheelRunLoad", max_workers=size)
        super().start()

    def __str__(self):
        return f"{self.__loop}"

    def insertTask(self,task,ttl):
        if (self.__probe + ttl) > self.__max:
            self.__max = ttl + self.__probe
            self.__loop[self.__max] = []
        key = self.__probe + ttl
        if key in self.__loop:
            self.__loop[key].append(task)
        else:
            self.__loop[key] = []
            self.__loop[key].append(task)
        self.__task += 1

    def getOldTaskSize(self):
        return self.__old
    def getAllTaskSize(self):
        return self.__task
    def getIsPool(self):
        return self.__isPool

