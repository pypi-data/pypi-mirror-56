from enum import IntEnum

__all__ = [
    'Aggregation',
    'Enrichment',
    'Maneuver',
    'DrivingPrimitiveInDrive',
    'SignalAggregatedBaseModel',

    'TimeBase',
]

Aggregation = None
Enrichment = None
Maneuver = None
DrivingPrimitiveInDrive = None
SignalAggregatedBaseModel = None


class TimeBase(IntEnum):
    """
    The aggregation and enrichment time base
    """
    Second = 0
    Decisecond = 1
    Centisecond = 2
