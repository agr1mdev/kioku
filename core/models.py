from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, Date

class Base(DeclarativeBase):
    pass

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Concept(Base):
    __tablename__ = "concepts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject_id = Column(Integer)
    repetitions = Column(Integer, default=0)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    next_review = Column(Date,nullable=True) 

class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True)
    front = Column(String)
    back = Column(String)
    concept_id = Column(Integer)
    repetitions = Column(Integer, default=0)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    next_review = Column(Date,nullable=True) 






        