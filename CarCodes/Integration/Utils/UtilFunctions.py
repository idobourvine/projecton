import math


def clamp_to_0_360(deg):
    """
    Returns the equivalent angle in the range [0, 360]
    """
    return deg % 360


def clamp_to_180(deg):
    """
    Returns the equivalent angle in the range [-180, 180]
    """
    deg %= 360
    if deg > 180:
        deg -= 180
    return deg


def to_degs(angle):
    return angle * (180 / math.pi)


def pythagoras(nums):
    return math.sqrt(sum([x ** 2 for x in nums]))
