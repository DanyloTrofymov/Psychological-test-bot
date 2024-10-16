from dataclasses import dataclass


@dataclass
class HelpingCenterResponse:
    id: int
    name: str
    workingHours: str
    phone: str