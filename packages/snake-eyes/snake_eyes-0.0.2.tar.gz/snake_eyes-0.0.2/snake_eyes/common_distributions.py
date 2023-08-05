from snake_eyes import BernoulliDistribution, Distribution, NormalDistribution, UniformDistribution, \
    UniformDiscreteDistribution

radermacher_distribution: Distribution[int] = (2 * BernoulliDistribution(0.5) - 1)
standard_normal_distribution: Distribution[float] = NormalDistribution(0, 1)
standard_uniform_distribution: Distribution[float] = UniformDistribution(0, 1)


def die(sides, n=1) -> Distribution[int]:
    if n != 1:
        return n @ die(sides)
    return UniformDiscreteDistribution(1, sides)


coin: Distribution[int] = die(2)
d6: Distribution[int] = die(6)
