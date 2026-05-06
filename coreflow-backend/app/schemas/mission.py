from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.mission import MissionType, MissionSource
from app.models.user import EnergyState

class MissionBase(BaseModel):
    title: str
    description: Optional[str] = None
    source: MissionSource = MissionSource.manual
    type: MissionType
    energy_cost: EnergyState
    status: str = "pending"
    base_priority: int = 0

class MissionCreate(MissionBase):
    user_id: UUID

class MissionResponse(MissionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
