"""Data generators for big_O module."""

import random
import string

# TODO: how to apply this to functions with multiple arguments?
from itertools import product


def n_(n):
    """ Return N. """
    return n


def range_n(n, start=0):
    """ Return the sequence [start, start+1, ..., start+N-1]. """
    return list(range(start, start + n))


def integers(n, min_, max_):
    """ Return sequence of N random integers between min_ and max_ (included).
    """
    return [random.randint(min_, max_) for _ in range(n)]


def large_integers(n):
    """ Return sequence of N large random integers. """
    return [random.randint(-50, 50) * 1000000 + random.randint(0, 10000) for _ in range(n)]


def strings(n, chars=string.ascii_letters):
    """ Return random string of N characters, sampled at random from `chars`.
    """
    return ''.join([random.choice(chars) for _ in range(n)])


class InputIterator(object):
    """Abstract class that produces data to use as function input."""

    def __init__(self, *args, end=None):
        for _ in args:
            if not isinstance(_, InputIterator):
                raise ValueError("Iterator {} must inherit `InputIterator`".format(_))
        self.args = args
        self.end = end
        self.end = all(map(lambda x: x.end, args))

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError("Subclasses have to implement this.")


class ZipIterator(InputIterator):
    """Join InputIterators, take one element per step from each iterator"""

    def __init__(self, *args):
        super().__init__(*args)
        self.iterator = zip(*self.args)

    def __next__(self):
        return self.iterator.__next__()


class ProductIterator(InputIterator):
    """Join InputIterators, produce all possible combinations"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.end:
            raise ValueError("`InputIterator` arguments of `ProductIterator` must have ")
        self.iterator = product(*self.args, repeat=2)

    def __next__(self):
        i = self.iterator.__next__()
        print(i)
        return i


class IncreaseInt(InputIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.last = 0

    def __next__(self):
        if self.last >= self.end:
            raise StopIteration()

        self.last += 1
        return self.last


class DecreaseInt(InputIterator):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.last = 0

    def __next__(self):
        if self.last <= self.end:
            raise StopIteration()

        self.last -= 1
        return self.last
