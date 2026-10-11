"""Controlled vocabularies for data levels and collection groups."""

from enum import Enum


class DataLevel(str, Enum):
    """Data level name"""

    DERIVED = "derived"
    RAW = "raw"
    SIMULATED = "simulated"


class Group(str, Enum):
    """Data collection group name"""

    BEHAVIOR = "behavior"
    EPHYS = "ephys"
    MSMA = "MSMA"
    OPHYS = "ophys"
    NBA = "NBA"
