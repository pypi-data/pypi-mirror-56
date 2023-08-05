from abc import ABC
from typing import Type, Union, Callable

from scipy.stats import rv_continuous, rv_discrete

import numpy as np

from snake_eyes import Distribution
from snake_eyes.buffered_distribution import BuffererMakerDistribution
from snake_eyes.bufferer import Bufferer
from snake_eyes.support_space import ContinuousSupportSpace

RV = Union[rv_discrete, rv_continuous]


def rv_bufferer_class(rv: RV):
    """
    Create a Bufferer subclass that wraps a scipy rv
    """
    class Ret(Bufferer):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.args = args
            self.kwargs = kwargs

        def get_buffer(self, size) -> np.ndarray:
            return rv.rvs(*self.args, size=size, **self.kwargs)

    return Ret


class RVAdapterBase(Distribution, ABC):
    """
    an mixin subclass that implements many methods with a frozen scipy.rv instance
    """
    def __init__(self, frozen):
        self.frozen = frozen

    def mean(self):
        return self.frozen.mean()

    def variance(self):
        return self.frozen.var()

    def deviation(self):
        return self.frozen.std()

    def cumulative_density(self, k):
        return self.frozen.cdf(k)

    def sample_mean(self, sample_size=256, abs_tol=0.0, rel_tol=1e-7, func: Callable[[float], float] = None):
        if func is None:
            self.mean()
        return self.frozen.expect(func)


def _rv_class(rv: RV):
    """
    create a common superclass for a generic rv
    """
    bufferer_cls = rv_bufferer_class(rv)

    class Ret(BuffererMakerDistribution[float], RVAdapterBase):
        def __init__(self, *args, **kwargs):
            BuffererMakerDistribution.__init__(self, bufferer_cls, args, kwargs)
            RVAdapterBase.__init__(self, rv(*args, **kwargs))

    return Ret


def rv_continuous_class(rv: rv_continuous, name: str = None, module: str = None, **kwargs) \
        -> Type[BuffererMakerDistribution[float]]:
    """
    create a distribution for a scipy.rv_continuous
    :param rv: the rv_continuous instance to wrap
    :param name: if set, sets the name of the class
    :param module: if set, sets the module of the class
    :param kwargs: additional attributes of the class to set
    """
    base = _rv_class(rv)

    class Ret(base):
        def probability(self, k):
            return self.frozen.pdf(k)

        def support_space(self):
            a, b = self.frozen.interval(1)
            return ContinuousSupportSpace(a, b)

    for k, v in kwargs.items():
        setattr(Ret, k, v)

    if module:
        Ret.__module__ = module
    if name:
        Ret.__qualname__ = Ret.__name__ = name

    return Ret


def rv_discrete_class(rv: rv_discrete, name: str = None, module: str = None, support_space_cls=None, **kwargs) \
        -> Type[BuffererMakerDistribution[float]]:
    """
    create a distribution for a scipy.rv_discrete
    :param rv: the rv_discrete instance to wrap
    :param name: if set, sets the name of the class
    :param module: if set, sets the module of the class
    :param support_space_cls: the class for the support space, called with the minimum and maximum of the distribution
    :param kwargs: additional attributes of the class to set
    """
    base = _rv_class(rv)

    class Ret(base):
        def probability(self, k):
            return self.frozen.pmf(k)

        def support_space(self):
            if support_space_cls:
                a, b = self.frozen.interval(1)
                # todo there is currently a bug in scipy that intervals for discrete values are offset by 1 on
                #  lower bound, fix
                return support_space_cls(a + 1, b)
            return None

    for k, v in kwargs.items():
        setattr(Ret, k, v)

    if module:
        Ret.__module__ = module
    if name:
        Ret.__qualname__ = Ret.__name__ = name

    return Ret
