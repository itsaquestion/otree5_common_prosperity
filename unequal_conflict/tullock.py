"""

"""


def tullock(x, y):
    """
    Tullock函数，返回x的胜率
    参数x和y分别为竞争投入，必须不小于0
    若x==y==0，返回(0.5, 0.5)

    >>> tullock(1,3)
    0.25

    >>> tullock(8,2)
    0.8

    >>> round(tullock(1,2),2)
    0.33

    >>> tullock(0,0)
    0.5

    >>> tullock(0,5)
    0.0

    >>> tullock(2,0)
    1.0

    >>> tullock(-1,2)
    Traceback (most recent call last):
    ...
    ValueError: x, y must >= 0

    >>> tullock(0,-1)
    Traceback (most recent call last):
    ...
    ValueError: x, y must >= 0

    """
    if x < 0 or y < 0:
        raise ValueError("x, y must >= 0")

    if x == y:
        return 0.5

    return x / (x + y)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
