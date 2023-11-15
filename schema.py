from fastapi import UploadFile
from pydantic import BaseModel
from typing import List

class Department(BaseModel):
    name: str
    sem: str

    class Config:
        orm_mode = True

class Course(BaseModel):
    intro: str
    name: str
    sem: str
    dept_id: int

    class Config:
        orm_mode = True

class Topic(BaseModel):
    name: str
    notes: str
    course_id: int

    class Config:
        orm_mode = True

class Questions(BaseModel):
    content: str
    topic_id: int
    options: List[str]
    answer: str
    pic: str
    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    sem: str
    dept_id: int

    class Config:
        orm_mode=True


class Result(BaseModel):
    answers: dict
    user_id: int
    score: float
    topic_id: int
    topic_name: str
    course_name: str
    
    class Config:
        orm_mode=True

