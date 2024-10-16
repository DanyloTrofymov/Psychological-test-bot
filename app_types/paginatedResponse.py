from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar('T')

@dataclass
class PaginatedResponse(Generic[T]):
    content: List[T]
    page: int
    limit: int
    total_elements: int
    total_pages: int