from __future__ import annotations
from enum import Enum
from dataclasses import dataclass


class RegimeType(str, Enum):
    SIX_BY_ONE = '6x1'
    FIVE_BY_TWO = '5x2'
    FOUR_BY_THREE = '4x3'

_REGIME_META = {
    RegimeType.SIX_BY_ONE: {
        'daily_hours': '6:20',
        'weekly_hours': 38,
        'days_off_per_week': 1,
    },
    RegimeType.FIVE_BY_TWO: {
        'daily_hours': '8:12',
        'weekly_hours': 41,
        'days_off_per_week': 2,
    },
    RegimeType.FOUR_BY_THREE: {
        'daily_hours': '6:15',
        'weekly_hours': 25,
        'days_off_per_week': 2,
    }
}


@dataclass(frozen=True)
class WorkRegime:
    regime: RegimeType

    @classmethod
    def from_string(cls, regime: str) -> WorkRegime:
        try:
            return cls(
                regime=RegimeType(regime),
            )
        
        except ValueError:
            raise ValueError(
                f'Invalid regime "{regime}". '
                f'Valid regimes: {[r.value for r in RegimeType]}'
            )

    @property
    def daily_hours(self) -> str:
        return _REGIME_META[self.regime]['daily_hours']

    @property
    def weekly_hours(self) -> int:
        return _REGIME_META[self.regime]['weekly_hours']

    @property
    def days_off_per_week(self) -> int:
        return _REGIME_META[self.regime]['days_off_per_week']
    
    def __str__(self) -> str:
        return self.regime.value

    def to_dict(self) -> dict:
        return {
            'regime': self.regime.value,
            'daily_hours': self.daily_hours,
            'weekly_hours': self.weekly_hours,
            'days_off_per_week': self.days_off_per_week,
        }
