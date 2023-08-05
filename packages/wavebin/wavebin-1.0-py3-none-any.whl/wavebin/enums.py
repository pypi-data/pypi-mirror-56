from enum import Enum

class WaveType(Enum):
    """
    Waveform types
    """

    UNKNOWN     = 0
    NORMAL      = 1
    PEAK_DETECT = 2
    AVERAGE     = 3
    LOGIC       = 6


class Units(Enum):
    """
    Unit types
    """

    UNKNOWN     = 0
    VOLTS       = 1
    SECONDS     = 2
    CONSTANT    = 3
    AMPS        = 4
    DECIBELS    = 5
    HERTZ       = 6


class DataType(Enum):
    """
    Data types
    """

    UNKNOWN     = 0
    FLOAT32     = 1
    FLOATMAX    = 2
    FLOATMIN    = 3
    UCHAR8      = 6
