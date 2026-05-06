import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class EnergyState(enum.Enum):
    high_focus = "high_focus"
    low_focus = "low_focus"
    neutral = "neutral"

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_battery = Column(SQLEnum(EnergyState), default=EnergyState.neutral)
    xp_points = Column(Integer, default=0)
    frozen_mode = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
