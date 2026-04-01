from __future__ import annotations
from dataclasses import dataclass
from datetime import time, datetime, timedelta


@dataclass(frozen=True)
class TimeSlot:
    start: time
    end: time

    def __post_init__(self):
        if not isinstance(self.start, time):
            raise TypeError("'start' deve ser um objeto datetime.time.")
        
        if not isinstance(self.end, time):
            raise TypeError("'fim' deve ser um objeto datetime.time.")
        
        if self.start == self.end:
            raise ValueError("'inicio' e 'fim' não podem ser iguais.")

        if self.duration_minutes > 24 * 60:
            raise ValueError("Um turno não pode ultrapassar 24 horas.")
    
    @classmethod
    def from_strings(cls, start: str, end: str) -> TimeSlot:
        def _parse(value: str) -> time:
            try:
                h, m = value.split(":")
                return time(int(h), int(m))
            
            except Exception:
                raise ValueError(f"Tempo inválido '{value}'. Use o formato 'HH:MM'.")

        return cls(start=_parse(start), end=_parse(end))

    @property
    def crosses_midnight(self) -> bool:
        return self.end < self.start

    @property
    def duration_minutes(self) -> int:
        base = datetime(2000, 1, 1)
        dt_start = datetime.combine(base.date(), self.start)
        dt_end = datetime.combine(base.date(), self.end)

        if self.crosses_midnight:
            dt_end += timedelta(days=1)

        return int((dt_end - dt_start).total_seconds() / 60)

    @property
    def duration_hours(self) -> float:
        return round(self.duration_minutes / 60, 2)

    def overlaps(self, other: TimeSlot) -> bool:
        base = datetime(2000, 1, 1)

        def to_dt(slot: TimeSlot, field: str) -> datetime:
            dt = datetime.combine(base.date(), getattr(slot, field))
            
            if field == "end" and slot.crosses_midnight:
                dt += timedelta(days=1)
            
            return dt

        start_a, end_a = to_dt(self, "start"), to_dt(self, "end")
        start_b, end_b = to_dt(other, "start"), to_dt(other, "end")

        return start_a < end_b and start_b < end_a

    def contains(self, timestamp: time) -> bool:
        if self.crosses_midnight:
            return timestamp >= self.start or timestamp < self.end
        
        return self.start <= timestamp < self.end

    def __str__(self) -> str:
        return f"{self.start.strftime('%H:%M')} → {self.end.strftime('%H:%M')}"

    def to_dict(self) -> dict:
        return {
            "start": self.start.strftime("%H:%M"),
            "end": self.end.strftime("%H:%M"),
            "duration_hours": self.duration_hours,
            "crosses_midnight": self.crosses_midnight,
        }
