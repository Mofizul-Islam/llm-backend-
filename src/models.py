from pydantic import BaseModel
from typing import List, Dict


class UserRequest(BaseModel):
    questions_count: int
    type: str
    context: str


class MCQQuestion(BaseModel):
    question: str
    options: Dict[str, str]
    answer: str
    explanation: str
    ref: str

    def __str__(self):
        return (f"Question: {self.question}\nOptions: {self.options}\nAnswer: {self.answer}\n"
                f"Explanation: {self.explanation}\nReference: {self.ref}")


class LongAnswerQuestion(BaseModel):
    question: str
    answer: str
    explanation: str
    ref: str

    def __str__(self):
        return (f"Question: {self.question}\nAnswer: {self.answer}\n"
                f"Explanation: {self.explanation}\nReference: {self.ref}")


class ShortAnswerQuestion(BaseModel):
    question: str
    answer: str
    explanation: str
    ref: str

    def __str__(self):
        return (f"Question: {self.question}\nAnswer: {self.answer}\n"
                f"Explanation: {self.explanation}\nReference: {self.ref}")


class MCQQuestionnaire(BaseModel):
    questions: List[MCQQuestion]

    def __str__(self):
        question_str = "\n".join([str(q) for q in self.questions])
        return f"MCQ Questions:\n{question_str}"


class LongAnswerQuestionnaire(BaseModel):
    questions: List[LongAnswerQuestion]

    def __str__(self):
        question_str = "\n".join([str(q) for q in self.questions])
        return f"Long Answer Questions:\n{question_str}"


class ShortAnswerQuestionnaire(BaseModel):
    questions: List[ShortAnswerQuestion]

    def __str__(self):
        question_str = "\n".join([str(q) for q in self.questions])
        return f"Short Answer Questions:\n{question_str}"
