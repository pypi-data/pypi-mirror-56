from ex_tools.exceptions import NotFound
from ex_tools.globals import Empty


def find(filter_f, iter_, default=Empty):
    """
    find function, finally.

    it takes the first object from a filter, and raises ex_tools.itertools.exceptions.NotFound when it fails,
    it returns default instead if default is set
    """
    if default is Empty:
        try:
            return next(filter(filter_f, iter_))
        except StopIteration:
            pass
        raise NotFound
    else:
        return next(filter(filter_f, iter_), default)
