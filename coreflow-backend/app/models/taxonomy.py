import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

topic_tags = Table(
    'topic_tags',
    Base.metadata,
    Column('topic_id', UUID(as_uuid=True), ForeignKey('topics.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

edital_topics = Table(
    'edital_topics',
    Base.metadata,
    Column('edital_id', UUID(as_uuid=True), ForeignKey('editais.id', ondelete='CASCADE'), primary_key=True),
    Column('topic_id', UUID(as_uuid=True), ForeignKey('topics.id', ondelete='CASCADE'), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)

class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(100))

    subjects = relationship("Subject", back_populates="discipline", cascade="all, delete")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    discipline_id = Column(UUID(as_uuid=True), ForeignKey('disciplines.id', ondelete='CASCADE'))
    name = Column(String(255), nullable=False)

    discipline = relationship("Discipline", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id', ondelete='CASCADE'))
    name = Column(String(255), nullable=False)
    knowledge_level = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)

    subject = relationship("Subject", back_populates="topics")
    tags = relationship("Tag", secondary=topic_tags)

class Edital(Base):
    __tablename__ = "editais"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="active")

    topics = relationship("Topic", secondary=edital_topics)
