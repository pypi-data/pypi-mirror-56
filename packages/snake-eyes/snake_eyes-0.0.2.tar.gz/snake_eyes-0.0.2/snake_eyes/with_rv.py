from math import floor, ceil

from scipy.stats import uniform, randint, norm, truncnorm, bernoulli, geom, hypergeom, poisson, zipf, triang

from snake_eyes.distribution import add, mul
from snake_eyes.from_rv import rv_continuous_class, rv_discrete_class
from snake_eyes.support_space import DiscreteWholeSupportSpace


class UniformDistribution(rv_continuous_class(uniform)):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        super().__init__(a, b - a)

    @add.implementor(symmetric=True)
    def add(self, other: float):
        return type(self)(self.a + other, self.b + other)

    @mul.implementor(symmetric=True)
    def mul(self, other: float):
        a = self.a
        b = self.b
        if other < 0:
            a, b = b, a
        return type(self)(a * other, b * other)

    def truncate(self, a=None, b=None):
        a = max(a, self.a) if a is not None else self.a
        b = min(b, self.b) if b is not None else self.b
        if (a, b) == (self.a, self.b):
            return self
        return type(self)(a, b)

    def args_str(self):
        return self.a, self.b


class UniformDiscreteDistribution(rv_discrete_class(randint, support_space_cls=DiscreteWholeSupportSpace)):
    def __init__(self, a, b):
        self.a = a
        self.b = b
        super().__init__(a, b + 1)

    def __neg__(self):
        return type(self)(-self.b, -self.a)

    @add.implementor(symmetric=True)
    def add(self, other: int):
        return type(self)(self.a + other, self.b + other)

    @mul.implementor(symmetric=True)
    def mul(self, other: float):
        if other != -1:
            return NotImplemented
        return -self

    def truncate(self, a=None, b=None):
        a = max(ceil(a), self.a) if a is not None else self.a
        b = min(floor(b), self.b) if b is not None else self.b
        if (a, b) == (self.a, self.b):
            return self
        return type(self)(a, b)

    def args_str(self):
        return self.a, self.b


class NormalDistribution(rv_continuous_class(norm)):
    def __init__(self, mu, sd):
        super().__init__(mu, sd)
        self.mu = mu
        self.sd = sd

    @add.implementor(symmetric=True)
    def add(self, other: float):
        return type(self)(self.mu + other, self.sd)

    @mul.implementor(symmetric=True)
    def mul(self, other: float):
        return type(self)(self.mu * other, self.sd * other)

    def truncate(self, min=None, max=None):
        if min is not None and max is not None:
            return TruncatedNormalDistribution(self.mu, self.sd, min, max)
        return super().truncate(min, max)


class TruncatedNormalDistribution(rv_continuous_class(truncnorm)):
    def __init__(self, mu, sd, a, b):
        self.a_adjusted = (a - mu) / sd
        self.b_adjusted = (b - mu) / sd
        super().__init__(mu, sd, self.a_adjusted, self.b_adjusted)
        self.mu = mu
        self.sd = sd
        self.a = a
        self.b = b

    def _inner(self):
        return NormalDistribution(self.mu, self.sd)

    @add.implementor(symmetric=True)
    def add(self, other: float):
        return (self._inner() + other).truncate(self.a + other, self.b + other)

    @mul.implementor(symmetric=True)
    def mul(self, other: float):
        a = self.a * other
        b = self.b * other
        if other < 0:
            a, b = b, a
        return (self._inner() * other).truncate(a, b)

    def truncate(self, a=None, b=None):
        a = max(a, self.a) if a is not None else self.a
        b = min(b, self.b) if b is not None else self.b
        if (a, b) == (self.a, self.b):
            return self

        return self._inner().truncate(a, b)

    def args_str(self):
        return self.mu, self.sd, self.a, self.b


BernoulliDistribution = rv_discrete_class(bernoulli, 'BernoulliDistribution', __name__,
                                          support_space_cls=DiscreteWholeSupportSpace)

ShiftedGeometricDistribution = rv_discrete_class(geom, 'ShiftedGeometricDistribution', __name__,
                                                 support_space_cls=DiscreteWholeSupportSpace)


class UnshiftedGeometricDistribution(ShiftedGeometricDistribution):
    def __init__(self, p):
        super().__init__(p, -1)
        self.p = p

    def args_str(self):
        return self.p

    def support_space(self):
        return super().support_space() + (-1)


HyperGeometricDistribution = rv_discrete_class(hypergeom, 'HyperGeometricDistribution', __name__,
                                               support_space_cls=DiscreteWholeSupportSpace)

PoissonDistribution = rv_discrete_class(poisson, 'PoissonDistribution', __name__,
                                        support_space_cls=DiscreteWholeSupportSpace)

ZipfDistribution = rv_discrete_class(zipf, 'ZipfDistribution', __name__,
                                     support_space_cls=DiscreteWholeSupportSpace)


class TriangularDistribution(rv_continuous_class(triang)):
    def __init__(self, a, b, peak):
        loc = a
        scale = b - loc
        c = (peak - loc) / scale
        super().__init__(c, loc, scale)
        self.a = a
        self.b = b
        self.peak = peak

    def args_str(self):
        return self.a, self.b, self.peak

    @add.implementor()
    def add(self, other: float):
        return type(self)(self.a + other, self.b + other, self.peak + other)

    @mul.implementor()
    def mul(self, other: float):
        a = self.a
        b = self.b
        if other < 0:
            a, b = b, a
        return type(self)(a * other, b * other, self.peak * other)
