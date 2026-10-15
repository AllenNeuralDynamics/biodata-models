"""Controlled vocabulary for data levels."""

from enum import Enum


class DataLevel(str, Enum):
    """Data level name"""

    DERIVED = "derived"
    RAW = "raw"
    SIMULATED = "simulated"
