from dataclasses import dataclass
from typing import Optional, List


@dataclass
class QuizAnswerResponse:
    id: int
    title: str
    score: int
    media_id: Optional[int] = None

@dataclass
class QuizQuestionResponse:
    id: int
    title: str
    created_at: str
    updated_at: str
    quiz_id: int
    answers: List[QuizAnswerResponse]
    subtitle: Optional[str] = None
    media_id: Optional[int] = None

@dataclass
class QuizCount:
  take: int
  questions: int

@dataclass
class QuizResponse:
    _count: QuizCount
    id: int
    title: str
    created_at: str
    updated_at: str
    active: bool
    max_score: int
    questions: List[QuizQuestionResponse]
    summary: Optional[str] = None
    subtitle: Optional[str] = None
    media_id: Optional[int] = None
    last_take_id: Optional[int] = None
        
