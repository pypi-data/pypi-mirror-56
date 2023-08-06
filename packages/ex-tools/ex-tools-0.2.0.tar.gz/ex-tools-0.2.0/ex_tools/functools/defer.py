from typing import Sequence, Union, Container, Type


class DeferContext:
    def __init__(self, *,
                 reverse=False,
                 suppress: Union[Type[BaseException], Container[Type[BaseException]]] = None):
        self._func_list = []
        self.reverse = reverse
        self.suppress = suppress

    def __call__(self, func_or_seq):
        if isinstance(func_or_seq, Sequence):
            self._func_list.extend(func_or_seq)
        else:
            self._func_list.append(func_or_seq)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for func in (reversed(self._func_list) if self.reverse else self._func_list):
            try:
                func()
            except Exception as e:
                del e  # relax
        if exc_type:
            if self.suppress:
                if isinstance(self.suppress, Container) and exc_type in self.suppress:
                    return True
                elif self.suppress == exc_type:
                    return True
            return False
        return True
