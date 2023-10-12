from core.classes.fuse_classes.iterable import FuseIterable


class FuseRange(FuseIterable):
    def __init__(self, stop, start=0, step=1):
        self.stop = stop
        self.start = start
        self.step = step
        if self.stop < self.start:  # invert so that stop is always greater than or equal to start
            self.stop, self.start = self.start, self.stop
        self._count = self.start - self.step  # this is so that f__next__ works on first iteration

    def f__next__(self):
        self._count += self.step
        if self._count < self.stop:
            return self._count
        raise StopIteration
