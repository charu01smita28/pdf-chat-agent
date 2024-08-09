from pydantic import BaseModel

class Answer(BaseModel):
    question_id: int
    answer_text: str
    confidence: float
