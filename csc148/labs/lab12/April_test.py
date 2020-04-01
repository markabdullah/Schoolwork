"""APril 2017 testing """


def width(list_, max_depth):
    """ Test
    >>> list_ = [0, 1]
    >>> width(list_, 1)
    2
    >>> list_ = [[0, 1], 2, [3, [[], 4]]]
    >>> width(list_, 4)
    4
    """
    num = 0
    for i in range(1, max_depth + 1):
        num = max(num, whelper(list_, i))
    return num


def whelper(list_, depth):
    """helper"""
    if isinstance(list_, int):
        return 0
    elif depth == 1:
        return len(list_)
    val = 0
    for item in list_:
        val += whelper(item, depth - 1)
    return val
