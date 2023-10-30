from enum import Enum


class MesaCoreFlag(Enum):
    NOT_DECLARED_ON_INIT = 0
    NON_TICK_BUSY_CLOCK = 1
    TICK_BUSY_CLOCK = 2
    CORESURFACE = 3
