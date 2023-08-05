from __future__ import annotations

from abc import abstractmethod, ABC
from bisect import bisect_right
from enum import Enum, auto
from itertools import product, count, chain
from math import sqrt
from numbers import Rational
from typing import Sequence, Optional, Iterable, Collection

from containerview.cached_iter import CacheIter
from containerview.sequence_view import SequenceView

from snake_eyes.util import prod, min_max_prod


class DistributionKind(Enum):
    """
    Describes whether a distribution kind is
    """
    Discrete = auto()
    # if a continuous support space includes values (a,b), it must also include all values between them
    Continuous = auto()


class SupportSpace(ABC):
    @abstractmethod
    def minimum(self):
        """
        :return: the smallest possible value the support can return, if different than -float('inf'),
         must be a value that the support includes
        """
        pass

    @abstractmethod
    def maximum(self):
        """
        :return: the largest possible value the support can return, if different than float('inf'),
         must be a value that the support includes
        """
        pass

    @abstractmethod
    def contains(self, k) -> Optional[bool]:
        """
        :return: whether the support space can return the value, or None if that can't be calculated
        """
        if self.minimum() > k or self.maximum() < k:
            return False
        if self.kind() == DistributionKind.Continuous:
            return True
        return None

    @abstractmethod
    def kind(self) -> Optional[DistributionKind]:
        """
        :return: the kind (discrete or continuous) of the support, or None if it is neither
        """
        pass

    @abstractmethod
    def is_finite(self):
        """
        :return: whether the support includes a finite number of values
        """
        pass

    def __iter__(self):
        """
        iterate over all possible values of the support, by default, raises error if the support is not discrete
        """
        if self.kind() != DistributionKind.Discrete:
            raise ValueError('support space is non-discrete')
        yield from ()

    def __add__(self, other: Rational):
        return SumSupportSpace((self, DiscreteFiniteSupportSpace((other,), True)))

    def __mul__(self, other: Rational):
        return ProdSupportSpace((self, DiscreteFiniteSupportSpace((other,), True)))

    def truncate(self, a, b) -> Optional[SupportSpace]:
        """
        truncate the support to exclude certain values
        """
        if a is None:
            a = -float('inf')
        if b is None:
            b = float('inf')

        if a <= self.minimum() and b >= self.maximum():
            return self
        if a > self.maximum() or b < self.minimum() or a > b:
            return None
        return TruncatedSupportSpace(self, a, b)

    def contains_space(self, other: SupportSpace):
        """
        :return: whether self wholly includes all values in other
        """
        s_k = self.kind()
        o_k = other.kind()
        if o_k == DistributionKind.Discrete and other.is_finite():
            return all(self.contains(t) for t in other)
        elif o_k == DistributionKind.Continuous:
            if s_k is None:
                return None
            if s_k != DistributionKind.Continuous:
                return False
            return self.contains(other.minimum()) and self.contains(other.maximum())
        else:
            return None

    def __lt__(self, other):
        return self.maximum() < other.minimum()

    def __le__(self, other):
        return self.maximum() <= other.minimum()


class DiscreteFiniteSupportSpace(SupportSpace):
    """
    A discrete, finite support space
    """

    def __init__(self, support: Sequence, is_sorted=False):
        self.support = support
        self.sorted = is_sorted

    def minimum(self):
        if self.sorted:
            return self.support[0]
        return min(self.support)

    def maximum(self):
        if self.sorted:
            return self.support[-1]
        return max(self.support)

    def contains(self, k) -> bool:
        if self.sorted:
            bis_ind = bisect_right(self.support, k)
            return self.support[bis_ind] == k
        return k in self.support

    def kind(self) -> DistributionKind:
        return DistributionKind.Discrete

    def is_finite(self):
        return True

    def __iter__(self):
        yield from super().__iter__()
        yield from self.support

    def __add__(self, other):
        return type(self)([s + other for s in self.support], self.sorted)

    def __mul__(self, other):
        return type(self)([s * other for s in self.support], self.sorted)

    def truncate(self, a, b):
        if a is None:
            a = -float('inf')
        if b is None:
            b = float('inf')

        if self.sorted and self.minimum() <= a and self.maximum() >= b:
            return self

        if self.sorted and (self.minimum() > b or self.maximum() < b):
            return None

        ss = tuple(s for s in self.support if a <= s <= b)
        if not ss:
            return None

        return type(self)(
            ss,
            self.sorted
        )


class DiscreteWholeSupportSpace(SupportSpace):
    """
    A discrete support space that only supports whole values in its range
    """

    def __init__(self, min, max=None):
        if min == -float('inf'):
            min = None
        elif min is not None:
            min = int(min)

        if max == float('inf'):
            max = None
        elif max is not None:
            max = int(max)

        self.min = min
        self.max = max

    def minimum(self):
        if self.min is not None:
            return self.min
        return -float('inf')

    def maximum(self):
        if self.max is not None:
            return self.max
        return float('inf')

    def contains(self, k) -> bool:
        return k % 1 == 0 \
               and (self.min is None or self.min <= k) \
               and (self.max is None or self.max >= k)

    def kind(self) -> Optional[DistributionKind]:
        return DistributionKind.Discrete

    def is_finite(self):
        return self.min is not None \
               and self.max is not None

    def __iter__(self):
        if self.min is None:
            if self.max is None:
                yield 0
                for i in count(1):
                    yield i
                    yield -i
            else:
                yield from count(self.max, -1)
        else:
            if self.max is None:
                yield from count(self.min)
            else:
                yield from range(self.min, self.max + 1)

    def __add__(self, other):
        n = None if self.min is None else self.min + other
        x = None if self.max is None else self.max + other
        return type(self)(n, x)

    def __mul__(self, other):
        n = None if self.min is None else self.min * other
        x = None if self.max is None else self.max * other
        if other < 0:
            n, x = x, n
        return type(self)(n, x)

    def truncate(self, a, b):
        if a is None:
            a = self.min
        elif self.min is not None:
            a = max(self.min, a)

        if b is None:
            b = self.max
        elif self.min is not None:
            b = min(self.max, b)

        if b < a:
            return None

        return type(self)(a, b)


class ContinuousSupportSpace(SupportSpace):
    """
    A continuous support space between two bounds
    """

    def __init__(self, minimum=-float('inf'), maximum=float('inf')):
        self._minimum = minimum
        self._maximum = maximum

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def contains(self, k) -> bool:
        return self._minimum <= k <= self._maximum

    def kind(self) -> DistributionKind:
        return DistributionKind.Continuous

    def __add__(self, other):
        return type(self)(self._minimum + other, self._maximum + other)

    def __mul__(self, other):
        n = self._minimum * other
        x = self._maximum * other
        if other < 0:
            n, x = x, n
        return type(self)(n, x)

    def truncate(self, a, b):
        if a is None:
            a = -float('inf')
        if b is None:
            b = float('inf')

        if self.minimum() <= a and self.maximum() >= b:
            return self

        a = max(a, self._minimum)
        b = min(b, self._maximum)

        if b < a:
            return None

        return type(self)(a, b)

    def is_finite(self):
        return False


class CompundSupportSpace(SupportSpace, ABC):
    def __init__(self, parts: Collection[SupportSpace]):
        self.parts = parts

    def is_finite(self):
        return all(p.is_finite() for p in self.parts)

    def __iter__(self):
        if any(not p.is_finite() for p in self.parts):
            # cantor tupling
            def _unpack(buffer, index):
                if len(self.parts) - len(buffer) == 1:
                    buffer.append(index)
                    return
                w = int((sqrt(8 * index + 1) - 1) // 2)
                buffer.append(index - (w ** 2 + w) // 2)
                _unpack(buffer, (w ** 2 + 3 * w) // 2 - index)

            def unpack(index):
                buffer = []
                _unpack(buffer, index)
                buffer.reverse()
                return buffer

            cached = [CacheIter(iter(p)) for p in self.parts]
            for i in count():
                indices = unpack(i)
                yield tuple(cache[i] for (cache, i) in zip(cached, indices))
        else:
            yield from product(*self.parts)


class ZipSupportSpace(CompundSupportSpace):
    """
    A zipping of support spaces
    """

    def minimum(self):
        return tuple(p.minimum() for p in self.parts)

    def maximum(self):
        return tuple(p.maximum() for p in self.parts)

    def contains(self, k) -> bool:
        return len(k) == len(self.parts) \
               and all(p.contains(ki) for (p, ki) in zip(self.parts, k))

    def kind(self) -> Optional[DistributionKind]:
        ret = None
        for p in self.parts:
            k = p.kind()
            if k is None:
                return k
            if ret is None:
                ret = k
            elif ret != k:
                return None
        return ret

    def __add__(self, other):
        return type(self)(p + other for p in self.parts)

    def __mul__(self, other):
        return type(self)(p * other for p in self.parts)


class SymmetricOpSupportSpace(CompundSupportSpace, ABC):
    """
    an abstract support space for combining support spaces
    """

    @classmethod
    @abstractmethod
    def func(cls, args: Iterable):
        pass

    @classmethod
    @abstractmethod
    def unfunc(cls, targ, known):
        pass

    @classmethod
    def _contains_from(cls, parts: SequenceView, targ):
        part = parts[0]
        parts = parts[1:]
        if not parts:
            return part.contains(targ)
        for s in part:
            new_targ = cls.unfunc(targ, s)
            if cls._contains_from(parts, new_targ):
                return True
        return False

    def contains(self, k):
        try:
            return self._contains_from(SequenceView(self.parts), k)
        except ValueError:
            return super().contains(k)

    def __iter__(self):
        yield from (self.func(t) for t in super().__iter__())

    def kind(self):
        ret = None
        for p in self.parts:
            k = p.kind()
            if k is None:
                return k
            if ret is None or k == DistributionKind.Continuous:
                ret = k
        return ret


class SumSupportSpace(SymmetricOpSupportSpace):
    """
    Compound sum of support spaces
    """

    @classmethod
    def func(cls, args):
        return sum(args)

    @classmethod
    def unfunc(cls, targ, k):
        return targ - k

    def minimum(self):
        return self.func(p.minimum() for p in self.parts)

    def maximum(self):
        return self.func(p.maximum() for p in self.parts)

    def __add__(self, other):
        parts = list(self.parts)
        parts[0] += other
        return type(self)(parts)


class ProdSupportSpace(SymmetricOpSupportSpace):
    """
    Compound product of support spaces
    """

    @classmethod
    def func(cls, args):
        return prod(args)

    @classmethod
    def unfunc(cls, targ, k):
        return targ / k

    def _minmax(self):
        mins = tuple(p.minimum() for p in self.parts)
        maxs = tuple(p.maximum() for p in self.parts)
        if any(m is None for m in mins) or any(m is None for m in maxs):
            return None, None
        return min_max_prod(mins, maxs)

    def minimum(self):
        return self._minmax()[0]

    def maximum(self):
        return self._minmax()[1]

    def __mul__(self, other):
        parts = list(self.parts)
        parts[0] *= other
        return type(self)(parts)


class ReciprocalSupportSpace(SupportSpace):
    """
    An inverse of a support space
    """

    def __init__(self, inner: SupportSpace):
        self.inner = inner

    def minimum(self):
        i_min = self.inner.minimum()
        i_max = self.inner.maximum()
        if (i_min < 0) != (i_max < 0):
            return -float('inf')
        return 1 / i_max

    def maximum(self):
        i_min = self.inner.minimum()
        i_max = self.inner.maximum()
        if (i_min < 0) != (i_max < 0):
            return float('inf')
        return 1 / i_min

    def kind(self) -> Optional[DistributionKind]:
        return self.inner.kind()

    def contains(self, k) -> bool:
        return self.inner.contains(1 / k)

    def __iter__(self):
        yield from (1 / v for v in self.inner)

    def is_finite(self):
        return self.inner.is_finite()


class TruncatedSupportSpace(SupportSpace):
    """
    a truncated support space
    """

    def __init__(self, inner, a, b):
        self.inner = inner
        if a is None:
            a = -float('inf')
        if b is None:
            b = float('inf')
        self.a = a
        self.b = b

    def minimum(self):
        return min(self.inner.minimum(), self.a)

    def maximum(self):
        return max(self.inner.maximum(), self.b)

    def contains(self, k) -> bool:
        return self.a <= k <= self.b and self.inner.contains(k)

    def kind(self) -> Optional[DistributionKind]:
        return self.inner.kind()

    def __iter__(self):
        yield from (
            k for k in self.inner
            if self.a <= k <= self.b
        )

    def __add__(self, other):
        return (self.inner + other).truncate(self.a + other, self.b + other)

    def __mul__(self, other):
        a = self.a * other
        b = self.b * other
        if other < 0:
            a, b = b, a
        return (self.inner * other).truncate(a, b)

    def truncate(self, a, b):
        if a is None:
            a = -float('inf')
        if b is None:
            b = float('inf')

        a, b = max(a, self.a), min(b, self.b)

        if b < a:
            return None

        return self.inner.truncate(a, b)

    def is_finite(self):
        return self.inner.is_finite()
