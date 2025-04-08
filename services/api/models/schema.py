from sqlalchemy import (
    Column, Integer, BigInteger, Text, Boolean, ForeignKey, TIMESTAMP, JSON
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    category = Column(Text, default='general')
    text = Column(Text, nullable=False)
    ideal_answer = Column(Text)
    ideal_audio_url = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class QuestionTag(Base):
    __tablename__ = 'question_tags'

    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True)
    tag = Column(Text, primary_key=True)

class UserQuestionHistory(Base):
    __tablename__ = 'user_question_history'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True)
    assigned_at = Column(TIMESTAMP, server_default=func.now())

class UserAnswer(Base):
    __tablename__ = 'user_answers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    answer_text = Column(Text)
    answer_audio_url = Column(Text)
    asr_transcript = Column(Text)
    gpt_feedback = Column(JSON)
    score_overall = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
