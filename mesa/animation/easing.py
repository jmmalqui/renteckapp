import math


def ease_in_sine(x):
    return 1 - math.cos((x * math.pi) / 2)


def ease_out_sine(x):
    return math.sin((x * math.pi) / 2)


def ease_in_out_sine(x):
    return -1 * (math.cos(math.pi * x) - 1) / 2


def ease_in_quad(x):
    return x * x


def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)


def ease_in_out_quad(x):
    if x < 0.5:
        return 2 * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 2) / 2


def ease_in_cubic(x):
    return x * x * x


def ease_out_cubic(x):
    return 1 - math.pow(1 - x, 3)


def ease_in_out_cubic(x):
    if x < 0.5:
        return 4 * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 3) / 2


def ease_in_quart(x):
    return x * x * x * x


def ease_out_quart(x):
    return 1 - math.pow(1 - x, 4)


def ease_in_out_quart(x):
    if x < 0.5:
        return 8 * x * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 4) / 2


def ease_in_quint(x):
    return x * x * x * x * x


def ease_out_quint(x):
    return 1 - math.pow(1 - x, 5)


def ease_in_out_quint(x):
    if x < 0.5:
        return 16 * x * x * x * x * x
    else:
        return 1 - math.pow(-2 * x + 2, 5) / 2


def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)


def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)


def ease_in_out_expo(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    if x < 0.5:
        return math.pow(2, 20 * x - 10) / 2
    else:
        return (2 - math.pow(2, -20 * x + 10)) / 2


def ease_in_circ(x):
    return 1 - math.sqrt(1 - math.pow(x, 2))


def ease_out_circ(x):
    return math.sqrt(1 - math.pow(x - 1, 2))


def ease_in_out_circ(x):
    if x < 0.5:
        return (1 - math.sqrt(1 - math.pow(2 * x, 2))) / 2
    else:
        return (math.sqrt(1 - math.pow(-2 * x + 2, 2)) + 1) / 2


def ease_in_back(x):
    c1 = 1.70158
    c2 = c1 + 1
    return c2 * x * x * x - c1 * x * x


def ease_out_back(x):
    c1 = 1.70158
    c2 = c1 + 1
    return 1 + c2 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)


def ease_in_out_back(x):
    c1 = 1.70158
    c2 = c1 * 1.525

    return (
        (math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        if x < 0.5
        else (math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2
    )


def ease_in_elastic(x):
    c1 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return math.pow(2, 10 * x - 10) * math.sin((x * 10 - 0.75) * c1)


def ease_out_elastic(x):
    c1 = (2 * math.pi) / 3
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return math.pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c1) + 1


class MesaAnimationCurves:
    EASE_IN_SINE = ease_in_sine
    EASE_OUT_SINE = ease_out_sine
    EASE_IN_OUT_SINE = ease_in_out_sine
    EASE_IN_QUAD = ease_in_quad
    EASE_OUT_QUAD = ease_out_quad
    EASE_IN_OUT_QUAD = ease_in_out_quad
    EASE_IN_CUBIC = ease_in_cubic
    EASE_OUT_CUBIC = ease_out_cubic
    EASE_IN_OUT_CUBIC = ease_in_out_cubic
    EASE_IN_QUART = ease_in_quart
    EASE_OUT_QUART = ease_out_quart
    EASE_IN_OUT_QUART = ease_in_out_quart
    EASE_IN_QUINT = ease_in_quint
    EASE_OUT_QUINT = ease_out_quint
    EASE_IN_OUT_QUINT = ease_in_out_quint
    EASE_IN_OUT_QUINT = ease_in_expo
    EASE_OUT_EXPO = ease_out_expo
    EASE_IN_OUT_EXPO = ease_in_out_expo
    EASE_IN_CIRC = ease_in_circ
    EASE_OUT_CIRC = ease_out_circ
    EASE_IN_OUT_CIRC = ease_in_out_circ
    EASE_IN_BACK = ease_in_back
    EASE_OUT_BACK = ease_out_back
    EASE_IN_OUT_BACK = ease_in_out_back
    EASE_IN_ELASTIC = ease_in_elastic
    EASE_OUT_ELASTIC = ease_out_elastic
