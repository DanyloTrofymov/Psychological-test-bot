from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthRequest:
    auth_date: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id: int
    photo_url: Optional[str] = None
    hash: str