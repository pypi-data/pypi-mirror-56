from __future__ import annotations

from abc import ABC, abstractmethod
from inspect import isabstract
from typing import Dict, FrozenSet, Tuple, Any, Iterable, Iterator

from dyndis import MultiDispatch, Self
import numpy as np

BUFFER_SIZE = 4096

empty_frozenset = frozenset()

add = MultiDispatch('__add__')
mul = MultiDispatch('__mul__')


class Bufferer(ABC, Iterator):
    """
    An infinite, self-filling buffer for non-deterministic functions
    """
    cache: Dict[Tuple[Tuple, FrozenSet[Tuple[Any, Any]]], Bufferer]

    @classmethod
    def make(cls, args, kwargs=None) -> Bufferer:
        """
        if the class cache contains a buffer of equal parameters, return it, if not create a new one and cache
         it for future use
        """
        fs = empty_frozenset if not kwargs else frozenset(kwargs.items())
        key = args, fs
        ret = cls.cache.get(key)
        if ret is None:
            ret = cls.cache[key] = cls(*args, **(kwargs or {}))
        return ret

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not isabstract(cls):
            cls.cache = {}

    def __init__(self):
        self.buffer = []
        self.next_index = 0

    @abstractmethod
    def get_buffer(self, size) -> np.ndarray:
        """
        :return: a valid np array, buffer must be of exactly size `size`
        """
        pass

    def __next__(self):
        """
        :return: the next element in the generated buffer, generates a new buffer if necessary
        """
        if len(self.buffer) == self.next_index:
            self.buffer = self.get_buffer(BUFFER_SIZE)
            self.next_index = 1
            return self.buffer[0]
        ret = self.buffer[self.next_index]
        self.next_index += 1
        return ret

    def get_n(self, n) -> np.ndarray:
        """
        :return: an independent buffer of size n
        """

        if not len(self.buffer):
            self.buffer = self.get_buffer(max(n, BUFFER_SIZE))

        ret = np.empty(n, self.buffer.dtype)
        if self.next_index + n > len(self.buffer):
            first_part_end = len(self.buffer) - self.next_index
            ret[0:first_part_end] = self.buffer[self.next_index:]
            self.buffer = self.get_buffer(BUFFER_SIZE + n - first_part_end)
            ret[first_part_end:] = self.buffer[BUFFER_SIZE:]
            self.buffer.resize((BUFFER_SIZE,), refcheck=False)
            self.next_index = 0
        else:
            ret[:] = self.buffer[self.next_index: self.next_index + n]
            self.next_index += n

        return ret

    __radd__ = __add__ = add.op()
    __rmul__ = __mul__ = mul.op()

    def reciprocal(self):
        return InvBufferer.make((self,))

    def __neg__(self):
        return -1 * self

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __truediv__(self, other):
        if isinstance(other, Bufferer):
            return self * other.reciprocal()
        return self * (1 / other)

    def __rtruediv__(self, other):
        return other * self.reciprocal()

    @add.implementor(symmetric=True)
    def add(self, other: Any):
        if isinstance(other, Bufferer):
            return SumBufferer.make(((self, other),))
        if other == 0:
            return self
        return SumConstBufferer.make((self, other))

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        if isinstance(other, Bufferer):
            return ProdBufferer.make(((self, other),))
        if other == 1:
            return self
        return ProdConstBufferer.make((self, other))


class FuncBufferer(Bufferer):
    """
    A bufferer that uses a function to generate buffers
    """

    def __init__(self, func, args, kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.func = func

    def get_buffer(self, size) -> np.ndarray:
        return self.func(*self.args, size=size, **self.kwargs)


def bufferer(func, name=None):
    class Ret(FuncBufferer):
        def __init__(self, *args, **kwargs):
            super().__init__(func, args, kwargs)

    Ret.__name__ = name or func.__name__
    return Ret


class SumBufferer(Bufferer):
    """
    A bufferer representing a sum of multiple bufferers
    """

    def __init__(self, parts: Iterable[Bufferer]):
        super().__init__()
        self.parts = tuple(parts)

    def get_buffer(self, size) -> np.ndarray:
        return np.sum([p.get_buffer(size) for p in self.parts], axis=0)

    def __add__(self, other):
        return type(self)(self.parts + (other,))

    def __radd__(self, other):
        return type(self)((other,) + self.parts)


class ProdBufferer(Bufferer):
    """
    A bufferer representing a product of multiple bufferers
    """

    def __init__(self, parts: Iterable[Bufferer]):
        super().__init__()
        self.parts = tuple(parts)

    def get_buffer(self, size) -> np.ndarray:
        return np.prod([p.get_buffer(size) for p in self.parts], axis=0)

    def __mul__(self, other):
        return type(self)(self.parts + (other,))

    def __rmul__(self, other):
        return type(self)((other,) + self.parts)


class InvBufferer(Bufferer):
    """
    A bufferer representing the inverse of a bufferer
    """

    def __init__(self, inner: Bufferer):
        super().__init__()
        self.inner = inner

    def get_buffer(self, size) -> np.ndarray:
        return 1 / self.inner.get_buffer(size)

    def reciprocal(self):
        return self.inner


class SumConstBufferer(Bufferer):
    """
    A bufferer representing a sum of a bufferers and a constant
    """

    def __init__(self, inner: Bufferer, const):
        super().__init__()
        self.inner = inner
        self.const = const

    def get_buffer(self, size) -> np.ndarray:
        return self.inner.get_buffer(size) + self.const

    @add.implementor(symmetric=True)
    def add(self, other: Any):
        if isinstance(other, Bufferer):
            return NotImplemented
        return self.inner + (self.const + other)

    @add.implementor()
    def add(self, other: Self):
        return (self.inner + other.inner) + (self.const + other.const)

    @add.implementor(symmetric=True)
    def add(self, other: SumBufferer):
        return (other + self.inner) + self.const


class ProdConstBufferer(Bufferer):
    """
    A bufferer representing a product of a bufferers and a constant
    """

    def __init__(self, inner: Bufferer, const):
        super().__init__()
        self.inner = inner
        self.const = const

    def get_buffer(self, size) -> np.ndarray:
        return self.inner.get_buffer(size) * self.const

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        if isinstance(other, Bufferer):
            return NotImplemented
        return self.inner * (self.const * other)

    @mul.implementor()
    def mul(self, other: Self):
        return (self.inner * other.inner) * (self.const * other.const)

    @mul.implementor(symmetric=True)
    def mul(self, other: ProdBufferer):
        return (other * self.inner) * self.const


@bufferer
def ChoiceBufferer(options, p=None, *, size):
    return np.random.choice(options, p=p, size=size)
