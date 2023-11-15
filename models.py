from sqlalchemy import Column, ForeignKey, Integer, String, FLOAT, ARRAY, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Department(Base):
    __tablename__ = 'dept'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    sem=Column(String )

class Course(Base):
    __tablename__ = 'course'
    id=Column(Integer, primary_key=True, autoincrement=True)
    intro=Column(String)
    name=Column(String)
    sem=Column(String)
    dept_id=Column(Integer, ForeignKey("dept.id"))
    dept= relationship("Department")

class Topic(Base):
    __tablename__= 'topic'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String)
    notes=Column(String)
    course_id=Column(Integer, ForeignKey("course.id"))
    course=relationship("Course")


class Questions(Base):
    __tablename__='questions'
    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    content=Column(String)
    pic=Column(String)
    options=Column(ARRAY(String))
    answer=Column(String)
    explanation=Column(String)
    topic_id=Column(Integer, ForeignKey("topic.id"))
    topic=relationship("Topic")

class User(Base):
    __tablename__= "user"
    id= Column(Integer, primary_key=True, autoincrement=True)
    name= Column(String)
    email= Column(String)
    password= Column(String)
    sem=Column(String)
    dept_id= Column(Integer, ForeignKey("dept.id"))
    dept= relationship("Department")

class Result(Base):
    __tablename__="result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    answers=Column(JSONB)
    score=Column(FLOAT)
    topic_id=Column(Integer, ForeignKey("topic.id"))
    topic_name=Column(String)
    course_name=Column(String)
    user_id= Column(Integer, ForeignKey("user.id"))
    user=relationship(User)