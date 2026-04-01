from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterator


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self):
        if not isinstance(self.start, date):
            raise TypeError("'start' deve ser um objeto datetime.date")
        
        if not isinstance(self.end, date):
            raise TypeError("'end' deve ser um objeto datetime.date")
        
        if self.start > self.end:
            raise ValueError(f"'start' ({self.start}) não pode ser posterior ao 'end' ({self.end}).")

    @classmethod
    def from_strings(cls, start: str, end: str) -> DateRange:
        def _parse(value: str) -> date:
            try:
                return date.fromisoformat(value)
            
            except ValueError:
                raise ValueError(f"Data inválida '{value}'. Use o formato 'YYYY-MM-DD'.")
            
        return cls(start=_parse(start), end=_parse(end))

    @classmethod
    def from_today(cls, days: int) -> DateRange:
        today = date.today()
        return cls(start=today, end=today + timedelta(days=days - 1))

    @property
    def total_days(self) -> int:
        return (self.end - self.start).days + 1

    @property
    def business_days(self) -> int:
        return sum(1 for d in self._iterate_days() if d.weekday() < 5)

    @property
    def weekend_days(self) -> int:
        return self.total_days - self.business_days

    def business_days_with_holidays(self, holidays: list[date]) -> int:
        holidays_set = set(holidays)
        return sum(1 for d in self._iterate_days() if d.weekday() < 5 and d not in holidays_set)

    def overlaps(self, other: DateRange) -> bool:
        return self.start <= other.end and other.start <= self.end

    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end

    def extend(self, days: int) -> DateRange:
        return DateRange(start=self.start, end=self.end + timedelta(days=days))

    def split_by_month(self) -> list[DateRange]:
        result = []
        current = self.start

        while current <= self.end:
            if current.month == 12:
                end_of_month = date(current.year + 1, 1, 1) - timedelta(days=1)
            
            else:
                end_of_month = date(current.year, current.month + 1, 1) - timedelta(days=1)

            partial_end = min(end_of_month, self.end)
            result.append(DateRange(start=current, end=partial_end))
            current = partial_end + timedelta(days=1)

        return result

    def _iterate_days(self) -> Iterator[date]:
        current = self.start
        while current <= self.end:
            yield current
            current += timedelta(days=1)

    def __str__(self) -> str:
        return f"{self.start.isoformat()} → {self.end.isoformat()} ({self.total_days}d)"

    def to_dict(self) -> dict:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "total_days": self.total_days,
            "business_days": self.business_days,
            "weekend_days": self.weekend_days,
        }
