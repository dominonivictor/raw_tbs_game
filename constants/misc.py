from enum import Enum

class sizes:
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    HUGE = "HUGE"
    Q_MARK = "???"    

def promote(value):
    return {
        SMALL: MEDIUM,
        MEDIUM: LARGE,
        LARGE: HUGE,
        HUGE: Q_MARK
    }.get(value, SMALL)

def add_sizes(one: str, other: str):
    if one == other:
        return promote(one)
    else:
        return one if gt_size(one, other) else other

def gt_size(one: str, other: str):
    values = [SMALL, MEDIUM, LARGE, HUGE]

    return values.index(one) > values.index(other)