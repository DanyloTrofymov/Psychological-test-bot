from dataclasses import dataclass
from typing import Optional, List

@dataclass
class TakeAnswerRequest:
    questionId: int
    answerId: int


@dataclass
class TakeRequest:
    quizId: int
    answers: List[TakeAnswerRequest]