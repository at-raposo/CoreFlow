import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.user import EnergyState
import enum

class MissionType(enum.Enum):
    theory = "theory"
    exercise = "exercise"
    flashcard = "flashcard"
    routine = "routine"

class MissionSource(enum.Enum):
    jupiterweb = "jupiterweb"
    qconcursos = "qconcursos"
    manual = "manual"

mission_tags = Table(
    'mission_tags',
    Base.metadata,
    Column('mission_id', UUID(as_uuid=True), ForeignKey('missions.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Mission(Base):
    __tablename__ = "missions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    description = Column(String)
    source = Column(SQLEnum(MissionSource), default=MissionSource.manual)
    type = Column(SQLEnum(MissionType))
    energy_cost = Column(SQLEnum(EnergyState), nullable=False)
    status = Column(String(50), default="pending")
    base_priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    tags = relationship("Tag", secondary=mission_tags)
