from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str

class QuestionCreate(BaseModel):
    title: str
    complexity: int
    type: str
    options: str
    correct_answers: list = []
    max_score: int

class ExamCreate(BaseModel):
    title: str
    duration: int
    ques_list: list = []

class UserCreate(BaseModel):
    full_name: str
    email: str
    role: str
    disabled: bool

class TokenCreate(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

class UserInDB(UserCreate):
    hashed_password: str
