from core.classes.fuse_classes.base import FuseClass


class FuseIterable(FuseClass):
    def __init__(self):
        pass

    def f__iter__(self):
        return self

    def f__next__(self):
        pass