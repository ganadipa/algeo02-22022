from threading import Thread


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


# def add(n1, n2):
#     result = n1 + n2
#     return result


# t = CustomThread(target=add, args=(1, 2))
# t.start()
# print(t.join())
