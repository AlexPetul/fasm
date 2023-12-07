from slugify import slugify
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    event,
)
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from src.db.config import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    slug = Column(String(200), unique=True)
    gpt_hint = Column(String, nullable=True)

    @validates("name")
    def convert_name_to_slug(self, key, value):
        self.slug = slugify(value)
        return value


@event.listens_for(Section, "before_insert")
def receive_before_insert(mapper, connection, target):
    if not target.slug:
        target.slug = slugify(target.name)


@event.listens_for(Section, "before_update")
def receive_before_update(mapper, connection, target):
    if not target.slug:
        target.slug = slugify(target.name)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    user_answer = Column(Text, nullable=True)
    gpt_answer = Column(Text, nullable=True)
    reviewer_answer = Column(Text, nullable=True)
    for_review = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    section_id = Column(Integer, ForeignKey("sections.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
