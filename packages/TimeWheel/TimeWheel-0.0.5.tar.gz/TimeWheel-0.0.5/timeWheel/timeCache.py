import threading
import time
import shelve
class TimeCache(threading.Thread):
    __oninit = int(time.time())
    __probe = 0
    __loop = {}
    __max = 10
    __errors = []
    __index = {}
    __L1 = {}
    def __init__(self):
        self.__cache = shelve.open("TimeCacheObject.db", "c")
        super().__init__()
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
                            self.Del(i)
                        except Exception as e:
                            self.__errors.append(str(e))
                    self.__loop[self.__probe] = []
            if len(self.__errors) > 0:
                print(self.__errors.pop())

    def start(self):
        super().start()

    def __str__(self):
        return f"{self.__loop}"
    def __getKey(self,ttl):
        if (self.__probe + ttl) > self.__max:
            self.__max = ttl + self.__probe
            self.__loop[self.__max] = []
        key = self.__probe + ttl
        return key
    def Set(self,name,val,ttl):
        if name not in self.__index:
            key = self.__getKey(ttl)
            if key in self.__loop:
                self.__loop[key].append(name)
            else:
                self.__loop[key] = []
                self.__loop[key].append(name)
        else:
            key = self.__index.get(name)
            if key in self.__loop:
                if name in self.__loop[key]:
                    self.__loop[key].remove(name)
            key = self.__getKey(ttl)
            if key in self.__loop:
                self.__loop[key].append(name)
            else:
                self.__loop[key] = []
                self.__loop[key].append(name)
        self.__cache[name] = val
        self.__index[name] = key
        if ttl < 30:
            self.__L1[name] = val

    def Get(self,name):
        if self.__L1.get(name):
            return self.__L1.get(name)
        return self.__cache.get(name)

    def Del(self,name):
        if self.__cache.get(name):
            del self.__cache[name]
            if name in self.__index:
                del self.__index[name]
        if self.__L1.get(name):
            del self.__L1[name]

if __name__ == '__main__':
    a = TimeCache()
    a.start()
    a.Set("A","1",1)
    a.Set("A", "1", 1)
    a.Set("A", "1", 1)
    a.Set("A", "1", 1)
    a.Set("A", "2", 5)
    print(a.Get("A"))
    time.sleep(6)
    print(a.Get("A"))