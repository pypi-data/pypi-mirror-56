import inspect
from abc import ABC, abstractmethod
from collections import deque
from math import log

"""
time-complexity (aka "Big O" or "Big Oh") of various operations in current CPython
    https://wiki.python.org/moin/TimeComplexity

Lecture: Complexity of Python Operations
    https://www.ics.uci.edu/~pattis/ICS-33/lectures/complexitypython.txt
"""


class CallMetric(ABC):
    """
        Average case complexities

        Generally, 'n' is the number of elements currently in the container.
        'k' is either the value of a parameter or the number of elements in the parameter.

        As in:  https://wiki.python.org/moin/TimeComplexity
        TODO: How should this be weighted ? C functions are faster
            The resulting value should be somewhat equivalent to counting bytecode instructions
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.instance = kwargs.get('instance')

    @staticmethod
    def is_primitive(value):
        return type(value) in [int, float, bool, str]

    @property
    @abstractmethod
    def value(self):
        raise NotImplementedError("Must be implemented by subclass.")


class Constant(CallMetric):
    """O(1)"""

    @property
    def value(self):
        return 1


class ArgsLengthLinear(CallMetric):
    @property
    def value(self):
        return len(self.args)


class FirstArgLengthLinear(CallMetric):
    @property
    def value(self):
        if inspect.isgenerator(self.args[0]):
            return len(list(self.args[0]))

        return len(self.args[0])


class SelfLengthLinear(CallMetric):
    @property
    def value(self):
        return len(self.instance)


class LastArgLengthLinear(CallMetric):
    @property
    def value(self):
        return len(self.args[-1])


class FirstArgLengthLogarithmic(CallMetric):
    @property
    def value(self):
        return len(self.args[0]) * log(len(self.args[0]), 10)


class SelfLengthLogarithmic(CallMetric):
    @property
    def value(self):
        return len(self.instance) * log(len(self.instance), 10)


class Pop(CallMetric):
    @property
    def value(self):
        if not self.args or self.args[0] == -1:
            # O(1), list.pop()
            return 1
        # O(N-i), list.pop(i)
        return len(self.instance) - (self.args[0] % len(self.instance))


class ContainerMultiply(CallMetric):
    """
    O(n*k), 'k' is the value of the parameter.
    """

    @property
    def value(self):
        return len(self.instance) * self.args


class Union(CallMetric):
    @property
    def value(self):
        return len(self.instance) + len(self.args[0])


class Intersection(CallMetric):
    @property
    def value(self):
        if isinstance(self.args[0], set):
            return min(len(self.instance), len(self.args[0]))
        return max(len(self.instance), len(self.args[0]))


"""
Map of Python builtin methods to average case time-complexity.
All complexity classes are based on the CPython implementation.
"""
avg_builtin_method_complexity = {
    # List
    list.copy.__qualname__: SelfLengthLinear,
    list.append.__qualname__: Constant,
    list.pop.__qualname__: Pop,
    list.insert.__qualname__: SelfLengthLinear,
    list.extend.__qualname__: FirstArgLengthLinear,
    list.sort.__qualname__: SelfLengthLogarithmic,
    list.index.__qualname__: SelfLengthLinear,
    list.clear.__qualname__: Constant,
    list.remove.__qualname__: SelfLengthLinear,
    list.count.__qualname__: SelfLengthLinear,
    list.reverse.__qualname__: SelfLengthLinear,
    list.__reversed__.__qualname__: SelfLengthLinear,
    list.__getitem__.__qualname__: Constant,
    list.__setitem__.__qualname__: Constant,
    list.__len__.__qualname__: Constant,
    list.__delitem__.__qualname__: SelfLengthLinear,
    list.__iter__.__qualname__: SelfLengthLinear,
    list.__contains__.__qualname__: SelfLengthLinear,
    list.__mul__.__qualname__: ContainerMultiply,

    # Tuple
    tuple.index.__qualname__: SelfLengthLinear,
    tuple.count.__qualname__: SelfLengthLinear,
    tuple.__contains__.__qualname__: SelfLengthLinear,
    tuple.__getitem__.__qualname__: Constant,
    tuple.__len__.__qualname__: Constant,
    tuple.__iter__.__qualname__: SelfLengthLinear,
    tuple.__mul__.__qualname__: ContainerMultiply,

    # Deque
    deque.copy.__qualname__: SelfLengthLinear,
    deque.append.__qualname__: Constant,
    deque.appendleft.__qualname__: Constant,
    deque.pop.__qualname__: Constant,
    deque.popleft.__qualname__: Constant,
    deque.extend.__qualname__: FirstArgLengthLinear,
    deque.extendleft.__qualname__: FirstArgLengthLinear,
    deque.rotate.__qualname__: FirstArgLengthLinear,
    deque.remove.__qualname__: SelfLengthLinear,
    deque.count.__qualname__: SelfLengthLinear,
    deque.index.__qualname__: SelfLengthLinear,
    # TODO: looking or modifying the middle of a deque is slow
    #   is constant complexity correct if we assume the avg case ?
    # deque.insert.__qualname__: Constant,
    # deque.clear.__qualname__: Constant,
    # deque.__getitem__.__qualname__: Constant,
    # deque.__setitem__.__qualname__: Constant,

    # Set
    set.union.__qualname__: Union,
    set.intersection.__qualname__: Intersection,
    set.difference.__qualname__: SelfLengthLinear,
    set.difference_update.__qualname__: FirstArgLengthLinear,
    set.symmetric_difference.__qualname__: SelfLengthLinear,
    set.symmetric_difference_update.__qualname__: FirstArgLengthLinear,
    # TODO:
    # set.pop.__qualname__: Constant,
    # set.copy.__qualname__: Constant,
    # set.update.__qualname__: Constant,
    # set.add.__qualname__: Constant,
    # set.remove.__qualname__: Constant,
    # set.clear.__qualname__: FirstArgLengthLinear,
    # set.discard.__qualname__: FirstArgLengthLinear,
    # set.intersection_update.__qualname__: FirstArgLengthLinear,
    # set.isdisjoint.__qualname__: FirstArgLengthLinear,
    # set.issubset.__qualname__: FirstArgLengthLinear,
    # set.issuperset.__qualname__: FirstArgLengthLinear,
    # set.__contains__.__qualname__: Constant,

    # Dict
    dict.copy.__qualname__: SelfLengthLinear,
    dict.get.__qualname__: Constant,
    dict.__getitem__.__qualname__: Constant,
    dict.__setitem__.__qualname__: Constant,
    dict.__delitem__.__qualname__: Constant,
    dict.__iter__.__qualname__: SelfLengthLinear,
}


class Range(CallMetric):
    @property
    def value(self):
        start = self.args[0]
        stop = self.args[1] if len(self.args) > 1 else 0
        step = self.args[2] if len(self.args) > 2 else 0
        return (stop - start) / step if step else 1


"""
Map of Python builtin functions to average case time-complexity.
All complexity classes are based on the CPython implementation.
"""

# TODO: complexity of (len, min, max) highly dependent on argument
avg_builtin_function_complexity = {
    abs.__qualname__: Constant,
    all.__qualname__: Constant,
    any.__qualname__: Constant,
    ascii.__qualname__: Constant,
    bin.__qualname__: Constant,
    chr.__qualname__: Constant,
    delattr.__qualname__: Constant,
    divmod.__qualname__: Constant,
    format.__qualname__: Constant,
    getattr.__qualname__: Constant,
    hasattr.__qualname__: Constant,
    hash.__qualname__: Constant,
    hex.__qualname__: Constant,
    id.__qualname__: Constant,
    iter.__qualname__: Constant,
    len.__qualname__: Constant,
    max.__qualname__: ArgsLengthLinear,
    min.__qualname__: ArgsLengthLinear,
    oct.__qualname__: Constant,
    ord.__qualname__: Constant,
    pow.__qualname__: Constant,
    print.__qualname__: Constant,
    repr.__qualname__: Constant,
    round.__qualname__: Constant,
    setattr.__qualname__: Constant,
    sorted.__qualname__: FirstArgLengthLogarithmic,
    sum.__qualname__: Constant,
    range.__qualname__: Range,
    reversed.__qualname__: FirstArgLengthLinear,
}
