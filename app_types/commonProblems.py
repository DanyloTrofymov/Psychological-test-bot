from dataclasses import dataclass


@dataclass
class CommonProblemsResponse:
    id: int
    title: str
    description: str
    url: str