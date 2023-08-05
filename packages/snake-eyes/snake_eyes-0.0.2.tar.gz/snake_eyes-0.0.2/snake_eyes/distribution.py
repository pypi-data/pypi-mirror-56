from __future__ import annotations

from abc import abstractmethod
from itertools import product
from math import sqrt
from numbers import Number, Real
from typing import Generic, TypeVar, Optional, Iterable, Union, Iterator, Any, Callable, Sequence

import numpy as np
from dyndis import MultiDispatch, Self

from snake_eyes.support_space import SupportSpace, DistributionKind, DiscreteFiniteSupportSpace, SumSupportSpace, \
    ProdSupportSpace, ReciprocalSupportSpace, ZipSupportSpace
from snake_eyes.util import prod, _maybe_parenthesise

add = MultiDispatch('__add__')
mul = MultiDispatch('__mul__')
div = MultiDispatch('__truediv__')
zip_ = MultiDispatch('zip')

T = TypeVar('T')


class Distribution(Iterator, Generic[T]):
    """
    A fully independent random variable
    """

    @staticmethod
    def coerce(x):
        """
        :return: x if it is a Distribution, or wrap it in a ConstDistribution otherwise
        """
        if isinstance(x, Distribution):
            return x
        return ConstDistribution(x)

    __radd__ = __add__ = add.op()
    __rmul__ = __mul__ = mul.op()
    __truediv__ = div.op()

    zip = zip_.method()

    @abstractmethod
    def get(self) -> T:
        """
        :return: roll a value from the distribution and return it
        """
        pass

    def get_n(self, n) -> Sequence[T]:
        """
        :return: roll n values from the distribution and return them as a sequence
        """
        yield from tuple(self.get() for _ in range(n))

    def mean(self) -> Optional[T]:
        """
        :return: the expected value of the distribution, or None if it cannot be exactly calculated
        :note: if the distribution has a finite support space and supports probability calls, this function
         has a default implementation
        """
        ss = self.support_space()
        if not ss or not ss.is_finite():
            return None
        ret = 0
        for x_i in ss:
            prob = self.probability(x_i)
            if prob is None:
                return None
            ret += prob * x_i
        return ret

    def variance(self) -> Optional[T]:
        """
        :return: the variance of the distribution, or None if it cannot be exactly calculated
        :note: if the distribution has a finite support space and supports probability calls, this function
         has a default implementation
        """
        ss = self.support_space()
        if not ss or not ss.is_finite():
            return None
        mean = 0
        sq_mean = 0
        for x_i in ss:
            prob = self.probability(x_i)
            if prob is None:
                return None
            pxi = prob * x_i
            mean += pxi
            sq_mean += pxi * x_i
        return sq_mean - mean ** 2

    def support_space(self) -> Optional[SupportSpace]:
        """
        :return: the support space of the distribution, or None if it cannot be exactly calculated
        """
        return None

    def cumulative_density(self, k) -> Optional[float]:
        """
        :return: the probability of the distribution returning a value less than or equal to k,
         or None if it cannot be exactly calculated
        :note: if the distribution has a finite support space and supports probability calls, this function
         has a default implementation
        """
        ss = self.support_space()
        if not ss:
            return None
        if k >= ss.maximum():
            return 1
        if k < ss.minimum():
            return 0
        if not ss.is_finite():
            return None
        ret = 0
        for x_i in ss:
            if x_i > k:
                continue
            prob = self.probability(x_i)
            if prob is None:
                return None
            ret += prob * x_i
        return ret

    def probability(self, k) -> Optional[float]:
        """
        :return: the probability of the distribution returning a value equal to k,
         or None if it cannot be exactly calculated. For continuous distributions, return the pmf of the distribution
        :note: if the distribution has a finite support space and supports probability calls, this function
         has a default implementation
        """
        ss = self.support_space()
        if not ss:
            return None
        if ss.contains(k) is False:
            return 0
        return None

    def deviation(self) -> Optional[T]:
        """
        :return: the support space of the distribution, or None if it cannot be exactly calculated
        """
        v = self.variance()
        if v is None:
            return v
        return sqrt(v)

    def __neg__(self) -> Distribution:
        """
        :return: a distribution that returns the negatives of the original distribution
        """
        return -1 * self

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def truncate(self, min=None, max=None):
        """
        :param min: The lower bound, or None
        :param max: The upper bound, or None
        :return: a truncated distribution, based on self and bound between min and max
        """
        if min is None and max is None:
            return self
        ss = self.support_space()
        if ss:
            a = ss.minimum()
            b = ss.maximum()
            if (min is None or a >= min) and (max is None or b <= max):
                return self
        return TruncatedDistribution(self, min, max)

    def reciprocal(self):
        """
        :return: a distribution reciprocal to this one
        """
        return ReciprocalDistribution(self)

    @div.implementor(-1)
    def truediv(self: Union[Self, Number], other):
        return self * other.reciprocal()

    @div.implementor(-1)
    def truediv(self, other: Real):
        return self * (1 / other)

    def __rtruediv__(self, other):
        return other * self.reciprocal()

    @add.implementor(priority=1, symmetric=True)
    def add(self, other: Number):
        if other == 0:
            return self
        return NotImplemented

    @add.implementor(priority=-1, symmetric=True)
    def add(self, other: object):
        return self + Distribution.coerce(other)

    @mul.implementor(priority=1, symmetric=True)
    def mul(self, other: Number):
        if other == 1:
            return self
        if other == 0:
            return self.coerce(other)
        return NotImplemented

    @mul.implementor(priority=-1, symmetric=True)
    def mul(self, other: object):
        return self * Distribution.coerce(other)

    @zip_.implementor()
    def zip_(self, other):
        return ZipDistribution((self, other))

    def approx_mean(self, **kwargs):
        """
        :param kwargs: forwarded to sample_mean, if necessary
        :return: the mean of the distribution, either exact or approximated using sample_mean
        """
        if 'func' not in kwargs:
            exact = self.mean()
            if exact is not None:
                return exact
        return self.sample_mean(**kwargs)

    def approx_variance(self, **kwargs):
        """
        :param kwargs: forwarded to sample_variance, if necessary
        :return: the variance of the distribution, either exact or approximated using sample_variance
        """
        exact = self.variance()
        if exact is not None:
            return exact
        return self.sample_variance(**kwargs)

    def approx_deviation(self, **kwargs):
        """
        :param kwargs: forwarded to sample_variance, if necessary
        :return: the standard deviation of the distribution, either exact or approximated using sample_variance
        """
        exact = self.deviation()
        if exact is not None:
            return exact
        return sqrt(self.approx_variance(**kwargs))

    def approx_cumulative_density(self, k, **kwargs):
        """
        :param kwargs: forwarded to sample_cumulative_density, if necessary
        :return: the cdf of the distribution, either exact or approximated using sample_cumulative_density
        """
        exact = self.cumulative_density(k)
        if exact is not None:
            return exact
        return self.sample_cumulative_density(k, **kwargs)

    def approx_probability(self, k, **kwargs):
        """
        :param kwargs: forwarded to sample_probability, if necessary
        :return: the probability of the distribution, either exact or approximated using sample_probability
        """
        exact = self.probability(k)
        if exact is not None:
            return exact
        return self.sample_probability(k, **kwargs)

    def sample_mean(self, sample_size=4096, func: Callable[[T], T] = None):
        """
        :param sample_size: the size of the sample
        :param func: a function to apply to the members (if set, calculates E[func(X)]
        :return: an approximate mean of the distribution calculated from a sample
        """
        batch = self.get_n(sample_size)
        if isinstance(batch, np.ndarray):
            if func:
                batch = func(batch)
            ret_s = np.sum(batch)
        else:
            if func:
                batch = (func(b) for b in batch)
            ret_s = sum(batch)
        return ret_s / sample_size

    def sample_variance(self, sample_size=4096):
        """
        :param sample_size: the size of the sample
        :return: an approximate variance of the distribution calculated from a sample
        """
        mean = self.approx_mean(sample_size=sample_size)
        return self.sample_mean(func=lambda x: x ** 2, sample_size=sample_size) - mean ** 2

    def sample_cumulative_density(self, k, sample_size=4096):
        """
        :param sample_size: the size of the sample
        :return: an approximate cdf of the distribution calculated from a sample
        """
        return self.sample_mean(func=lambda x: x <= k, sample_size=sample_size)

    def sample_probability(self, k, sample_size=4096, epsilon=None):
        """
        :param sample_size: the size of the sample
        :param epsilon: for continuous distributions, the epsilon of the approximation range.
         By default, uses the support space to generate an epsilon
        :return: an approximate pdf or pmf of the distribution calculated from a sample
        """
        ss = self.support_space()
        data = self.get_n(sample_size)
        if ss and ss.kind() == DistributionKind.Continuous:
            if epsilon is None:
                # by default assuming uniform, sqrt(sample_size) will be within epsilon
                epsilon = (ss.maximum() - ss.minimum()) / sqrt(sample_size)
            if isinstance(data, np.ndarray):
                total = np.sum((data <= (k + epsilon)) & ((k - epsilon) <= data))
            else:
                total = sum(1 for i in data if k - epsilon <= i <= k + epsilon)
            return total / (2 * epsilon * sample_size)
        else:
            if isinstance(data, np.ndarray):
                total = np.sum(data == k)
            else:
                total = sum(1 for i in data if i == k)
            return total / sample_size

    def __next__(self):
        """
        :return: equal to get()
        """
        return self.get()

    def __rmatmul__(self, other: int) -> Distribution:
        if other == 1:
            return self
        if other == 0:
            return NotImplemented
        if other < 0:
            return -(-other @ self)
        return sum(self for _ in range(other))

    def __lt__(self, other: T) -> Optional[float]:
        ret = self.cumulative_density(other)
        if ret is None:
            return None
        s = self.support_space()
        if s is not None and s.kind() != DistributionKind.Continuous:
            p = self.probability(other)
            if p is None:
                return None
            ret -= p
        return ret

    def __le__(self, other: T) -> Optional[float]:
        return self.cumulative_density(other)

    def __gt__(self, other: T) -> Optional[float]:
        return 1 - self.cumulative_density(other)

    def __ge__(self, other: T) -> Optional[float]:
        ret = 1 - self.cumulative_density(other)
        if ret is None:
            return None
        s = self.support_space()
        if s is not None and s.kind() != DistributionKind.Continuous:
            p = self.probability(other)
            if p is None:
                return None
            ret += p
        return ret

    def map(self, func: Callable[[T], F]) -> Distribution[F]:
        return MappedDistribution(self, func)


class ConstDistribution(Distribution[T], Generic[T]):
    """
    A distribution that always returns a constant value
    """

    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def get_n(self, n):
        return np.full(shape=n, fill_value=n)

    def mean(self):
        return self.value

    def variance(self):
        return 0

    def support_space(self):
        return DiscreteFiniteSupportSpace((self.value,), True)

    def cumulative_density(self, k):
        return int(k >= self.value)

    def probability(self, k):
        return int(k == self.value)

    def reciprocal(self):
        return type(self)(1 / self.value)

    def truncate(self, min=None, max=None):
        if (min is not None and min > self.value) \
                or (max is not None and max < self.value):
            raise ValueError("can't truncate a constant distribution outside its value")
        return self

    @add.implementor(symmetric=True)
    def add(self, other: Distribution):
        return self.value + other

    @mul.implementor(symmetric=True)
    def mul(self, other: Distribution):
        return self.value * other

    @add.implementor()
    def add(self, other: Self):
        return type(self)(self.value + other.value)

    @add.implementor(symmetric=True)
    def add(self, other: Number):
        return type(self)(self.value + other)

    @mul.implementor()
    def mul(self, other: Self):
        return type(self)(self.value * other.value)

    @mul.implementor(symmetric=True)
    def mul(self, other: Number):
        return type(self)(self.value * other)

    @div.implementor()
    def truediv(self, other):
        return type(self)(self.value / other.value)

    @div.implementor()
    def truediv(self, other: Number):
        return type(self)(self.value / other)

    @div.implementor()
    def truediv(self: Real, other):
        return type(self)(self / other.value)

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

    def __repr__(self):
        return type(self).__name__ + f"({self.value})"

    def __hash__(self):
        return hash(self.value)


class SymmetricOpDistribution(Distribution[T], Generic[T]):
    """
    Abstract class of composite distributions with a summetric and invertible function to compose them
    """

    def __init__(self, parts: Iterable[Distribution[T]]):
        parts = tuple(parts)
        assert len(parts) >= 2
        self.parts = parts

    @classmethod
    @abstractmethod
    def func(cls, parts):
        """
        combine multiple outputs of sub-distributions
        """
        pass

    def get(self):
        return self.func(p.get() for p in self.parts)

    def get_n(self, n):
        n_parts = tuple(p.get_n(n) for p in self.parts)
        for n_p in zip(*n_parts):
            yield self.func(n_p)

    @classmethod
    @abstractmethod
    def rev_func(cls, target, parts):
        """
        reverse of func, return None if no inverse exists
        :note: it should always be true that cls.func([cls.rev_func(target,x), *x]) == target
        """
        pass

    def probability(self, k):
        finite_parts = []
        finite_spaces = []
        other_parts = []
        for p in self.parts:
            ss = p.support_space()
            if ss is None or not ss.is_finite():
                other_parts.append(p)
                if len(other_parts) >= 2:
                    return None
            else:
                finite_spaces.append(ss)
                finite_parts.append(p)
        assert finite_parts
        if not other_parts:
            other_parts = finite_parts[-1:]
            del finite_parts[-1]
            del finite_spaces[-1]
        other, = other_parts
        total = 0
        for possibility in product(*finite_spaces):
            probs = tuple(part.probability(poss) for (part, poss) in zip(finite_parts, possibility))
            if None in probs:
                return None
            poss_prob = prod(probs)
            if poss_prob == 0:
                continue
            req = self.rev_func(k, possibility)
            if req is None:
                continue
            other_prob = other.probability(req)
            if other_prob is None:
                return None
            total += poss_prob * other_prob
        return total

    def sample_probability(self, k, **kwargs):
        discrete_finite_parts = []
        discrete_support_spaces = []
        other_parts = []
        for p in self.parts:
            ss = p.support_space()
            if ss is None or not ss.is_finite():
                other_parts.append(p)
            else:
                discrete_support_spaces.append(ss)
                discrete_finite_parts.append(p)

        if not discrete_finite_parts:
            return super().sample_probability(k, **kwargs)

        if not other_parts:
            other_parts = discrete_finite_parts[-1:]
            del discrete_finite_parts[-1]
            del discrete_support_spaces[-1]

        other = self.func(other_parts)
        total = 0

        for possibility in product(*discrete_support_spaces):
            probs = tuple(
                part.approx_probability(poss, **kwargs) for (part, poss) in zip(discrete_finite_parts, possibility)
            )
            if None in probs:
                return None
            poss_prob = prod(probs)
            if poss_prob == 0:
                continue
            req = self.rev_func(k, possibility)
            if req is None:
                continue
            other_prob = other.approx_probability(req, **kwargs)
            if other_prob is None:
                return None
            total += poss_prob * other_prob
        return total

    def __hash__(self):
        return hash((type(self), frozenset(self.parts)))

    def __eq__(self, other):
        return type(self) is type(other) and set(self.parts) == set(other.parts)


class SumDistribution(SymmetricOpDistribution[T], Generic[T]):
    """
    A distribution for a sum of other distributions
    """

    def mean(self):
        ret = 0
        for p in self.parts:
            m = p.mean()
            if m is None:
                return None
            ret += m
        return ret

    def variance(self):
        ret = 0
        for p in self.parts:
            m = p.variance()
            if m is None:
                return None
            ret += m
        return ret

    def support_space(self):
        spaces = []
        for p in self.parts:
            ss = p.support_space()
            if ss is None:
                return None
            spaces.append(ss)
        return SumSupportSpace(spaces)

    @classmethod
    def func(cls, parts):
        return sum(parts)

    @classmethod
    def rev_func(cls, target, parts):
        return target - sum(parts)

    @add.implementor(symmetric=True)
    def add(self, other: Distribution):
        p = self.parts + (other,)
        return type(self)(p)

    @mul.implementor(symmetric=True)
    def mul(self, other: Any):
        return sum(p * other for p in self.parts)

    @div.implementor()
    def truediv(self, other: Any):
        return sum(p / other for p in self.parts)

    def __str__(self):
        return " + ".join(_maybe_parenthesise(p) for p in self.parts)


class ProductDistribution(SymmetricOpDistribution[T], Generic[T]):
    """
    A distribution for a product of other distributions
    """

    @classmethod
    def func(cls, parts):
        return prod(parts)

    @classmethod
    def rev_func(cls, target, parts):
        if any(p == 0 for p in parts):
            return None
        return target / prod(parts)

    def mean(self):
        ret = 0
        for p in self.parts:
            m = p.mean()
            if m is None:
                return None
            ret *= m
        return ret

    def variance(self):
        variances = tuple(p.variance() for p in self.parts)
        means = tuple(p.mean() for p in self.parts)
        if any(d is None for d in variances) or any(m is None for m in means):
            return None
        sq_means = tuple(m * m for m in means)
        pos = zip(variances, sq_means)
        return sum(
            prod(x) for x in product(*pos)
        ) - prod(sq_means)

    def support_space(self):
        spaces = []
        for p in self.parts:
            ss = p.support_space()
            if ss is None:
                return None
            spaces.append(ss)
        return ProdSupportSpace(spaces)

    @mul.implementor(symmetric=True)
    def mul(self, other: Distribution):
        p = (*self.parts, other)
        return type(self)(p)

    def __str__(self):
        return " * ".join(_maybe_parenthesise(p) for p in self.parts)


class ReciprocalDistribution(Distribution[T], Generic[T]):
    """
    A distribution for a reciprocal of another distribution
    """

    def __init__(self, inner: Distribution):
        self.inner = inner
        ss = self.inner.support_space()
        if ss and ss.contains(0):
            raise ZeroDivisionError("can't get inverse of distribution that might return 0")

    def get(self):
        return 1 / self.inner.get()

    def get_n(self, n):
        yield from (1 / i for i in self.inner.get_n(n))

    def reciprocal(self):
        return self.inner

    def support_space(self):
        iss = self.inner.support_space()
        return iss and ReciprocalSupportSpace(iss)

    def probability(self, k):
        return self.inner.probability(1 / k)

    def __eq__(self, other):
        return type(self) is type(other) and set(self.inner) == set(other.inner)

    def __str__(self):
        return f"1/" + _maybe_parenthesise(self.inner)

    def __hash__(self):
        return hash((type(self), self.inner))


class ZipDistribution(Distribution[tuple]):
    """
    A distribution for a zipping of other distributions
    """

    def __init__(self, parts: Iterable[Distribution]):
        self.parts = tuple(parts)

    def get(self) -> T:
        return tuple(p.get() for p in self.parts)

    def get_n(self, n) -> T:
        n_parts = tuple(p.get_n(n) for p in self.parts)
        yield from zip(*n_parts)

    def mean(self) -> Optional[T]:
        ret = []
        for p in self.parts:
            m = p.mean()
            if m is None:
                return None
            ret.append(m)
        return ret

    def variance(self) -> Optional[T]:
        ret = []
        for p in self.parts:
            m = p.variance()
            if m is None:
                return None
            ret.append(m)
        return ret

    def deviation(self) -> Optional[T]:
        ret = []
        for p in self.parts:
            m = p.deviation()
            if m is None:
                return None
            ret.append(m)
        return ret

    def support_space(self) -> Optional[SupportSpace]:
        parts = []
        for p in self.parts:
            ss = p.support_space()
            if ss is None:
                return None
            parts.append(ss)
        return ZipSupportSpace(parts)

    def probability(self, k):
        if len(k) != len(self.parts):
            return 0
        ret = 1
        for (p, i) in zip(self.parts, k):
            m = p.probability(i)
            if m is None:
                return None
            if m == 0:
                return 0
            ret *= m
        return ret

    def sample_probability(self, k, **kwargs):
        if len(k) != len(self.parts):
            return 0
        ret = 1
        p: Distribution
        for (p, i) in zip(self.parts, k):
            m = p.approx_probability(i)
            if m is None:
                return None
            if m == 0:
                return 0
            ret *= m
        return ret

    @zip_.implementor()
    def zip_(self, other: Distribution):
        return ZipDistribution((*self.parts, other))

    @zip_.implementor()
    def zip_(self, other: Self):
        return ZipDistribution((*self.parts, *other.parts))

    @zip_.implementor()
    def zip_(self: Distribution, other: Self):
        return ZipDistribution((self, *other.parts))

    def __eq__(self, other):
        return type(self) is type(other) and self.parts == other.parts

    def __repr__(self):
        return type(self).__name__ + "(" + ", ".join(_maybe_parenthesise(p) for p in self.parts) + ")"

    def __hash__(self):
        return hash((type(self), self.parts))


class TruncatedDistribution(Distribution[T], Generic[T]):
    """
    A truncated wrapper for a distribution, re-rolling all results outsize the bounds
    """

    def __init__(self, inner: Distribution[T], min=None, max=None):
        self.inner = inner
        self.min = min
        self.max = max

    def get(self) -> T:
        for ret in self.inner:
            if self.min is not None and self.min > ret:
                continue
            if self.max is not None and self.max < ret:
                continue
            return ret

    def get_n(self, n) -> T:
        density = self._valid_density()
        if density is None:
            density = 1
        ret = []
        while len(ret) < n:
            buffer = (
                i for i in self.inner.get_n(int((n - len(ret)) / density))
                if (self.min is None or i >= self.min) and (self.max is None or i <= self.max)
            )
            ret.extend(buffer)
        if len(ret) >= n:
            del ret[n:]
        return ret

    def __neg__(self):
        n = -self.min if self.min else self.min
        x = -self.max if self.max else self.max
        return (-self.inner).truncate(x, n)

    @add.implementor(symmetric=True)
    def add(self, other: Number):
        n = self.min + other if self.min else self.min
        x = self.max + other if self.max else self.max
        return (self.inner + other).truncate(n, x)

    @mul.implementor(symmetric=True)
    def mul(self, other: Real):
        n = self.min * other if self.min else self.min
        x = self.max * other if self.max else self.max
        if other < 0:
            n, x = x, n
        return (self.inner * other).truncate(n, x)

    def truncate(self, min=None, max=None):
        if min is None or (self.min is not None and self.min > min):
            min = self.min

        if max is None or (self.max is not None and self.max < max):
            max = self.max

        if (min, max) == (self.min, self.max):
            return self

        return self.inner.truncate(min, max)

    def _valid_density(self):
        if self.max is not None:
            m = self.inner.cumulative_density(self.max)
            if m is None:
                return None
            ret = m
        else:
            ret = 1

        if self.min is not None:
            m = self.inner.cumulative_density(self.min)
            if m is None:
                return None
            ret -= m
        return ret

    def support_space(self):
        iss = self.inner.support_space()
        return iss and iss.truncate(self.min, self.max)

    def cumulative_density(self, k):
        vd = self._valid_density()
        if vd is None:
            return None
        f_a = 0
        if self.min is not None:
            f_a = self.inner.cumulative_density(self.min)
            if f_a is None:
                return None
        return (self.inner.cumulative_density(k) - f_a) / vd

    def probability(self, k):
        vd = self._valid_density()
        if vd is None:
            return None
        return self.inner.probability(k) / vd

    def __eq__(self, other):
        return type(self) is type(other) and (self.inner, self.min, self.max) == (other.inner, other.min, other.max)

    def __hash__(self):
        return hash((type(self), self.inner, self.min, self.max))


F = TypeVar('F')


class MappedDistribution(Distribution[T], Generic[F, T]):
    def __init__(self, inner: Distribution[F], func: Callable[[F], T]):
        self.inner = inner
        self.func = func

    def get(self) -> T:
        return self.func(self.inner.get())

    def get_n(self, n) -> Sequence[T]:
        return [self.func(i) for i in self.inner.get_n(n)]
