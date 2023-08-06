from functools import partial
from typing import Callable, Collection


class PipeClass:
    def __init__(self, queue):
        self.queue = queue

    def __or__(self, other: [Callable, Collection]):
        if callable(other):
            return PipeClass(self.queue + [other])
        if isinstance(other, Collection):
            return PipeClass(self.queue + [partial(*other)])

    def __call__(self, x):
        ret = x
        for func in self.queue:
            ret = func(ret)
        return ret

    def __repr__(self):
        return 'Pipe([{}])'.format(', '.join(map(str, self.queue)))


Pipe = PipeClass([])
