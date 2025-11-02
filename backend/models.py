from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class PuzzleRequest(BaseModel):
    difficulty: Difficulty
    user_id: str

class PuzzleResponse(BaseModel):
    question: str
    correct_answer: float
    difficulty: Difficulty
    puzzle_id: str

class AnswerRequest(BaseModel):
    user_id: str
    puzzle_id: str
    user_answer: float
    response_time: float

class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: float
    next_difficulty: Difficulty
    performance_stats: dict

class SessionSummary(BaseModel):
    user_id: str
    total_questions: int
    correct_answers: int
    accuracy: float
    average_response_time: float
    difficulty_history: List[Difficulty]
    recommendation: str