from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    and_,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (Index("idx_users_telegram_id", "telegram_id"),)


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    source_type = Column(String(50), nullable=False)
    source_id = Column(Integer, nullable=False)
    media_type = Column(String(50), nullable=False)
    url = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (Index("idx_media_source", "source_type", "source_id"),)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    category = Column(String(100), default="general")
    text = Column(Text, nullable=False)
    correct_answer = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    media = relationship(
        "Media",
        primaryjoin=lambda: and_(
            Media.source_id == Question.id,
            Media.source_type == "question",
        ),
        foreign_keys=[Media.source_id],
        viewonly=True,
    )

    __table_args__ = (Index("idx_questions_category_active", "category", "is_active"),)

    @property
    def correct_audio(self):
        return next((m for m in self.media if m.description == "correct_answer"), None)

    @property
    def illustrations(self):
        return [m for m in self.media if m.media_type == "image"]


class QuestionTag(Base):
    __tablename__ = "question_tags"

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )
    tag = Column(String(100), primary_key=True)

    __table_args__ = (Index("idx_question_tags_tag", "tag"),)


class UserQuestionHistory(Base):
    __tablename__ = "user_question_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    assigned_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (Index("idx_user_question_history_assigned_at", "assigned_at"),)


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    asr_transcript = Column(Text)
    gpt_feedback = Column(JSON)
    score_overall = Column(
        Integer, CheckConstraint("score_overall >= 0 AND score_overall <= 100")
    )
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship with Media for user's answer audio
    answer_media = relationship(
        "Media",
        primaryjoin=lambda: and_(
            Media.source_id == UserAnswer.id,
            Media.source_type == "user_answer",
        ),
        foreign_keys=[Media.source_id],
        viewonly=True,
    )

    # Relationship with Question
    question = relationship("Question")

    __table_args__ = (
        Index("idx_user_answers_user_question", "user_id", "question_id"),
    )


class UserQuota(Base):
    __tablename__ = "user_quotas"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    total_allowed = Column(Integer, default=10)
    used = Column(Integer, default=0)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
