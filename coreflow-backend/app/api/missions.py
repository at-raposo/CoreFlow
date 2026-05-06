from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.mission import Mission
from app.models.user import EnergyState
from app.schemas.mission import MissionResponse

router = APIRouter()

@router.get("/missions", response_model=List[MissionResponse])
def get_missions(
    energy_state: EnergyState = Query(EnergyState.neutral, description="The current energy battery state of the user"),
    db: Session = Depends(get_db)
):
    """
    ADHD Engine: Fetch and sort missions based on the current energy state.
    """
    # Fetch missions that match the energy state
    # In a more advanced implementation, we could just reorder them, but for now we filter and order by base priority
    
    query = db.query(Mission).filter(Mission.status == "pending")
    
    # Simple ADHD Engine Rule:
    if energy_state == EnergyState.high_focus:
        # High focus: we can show high energy missions and neutral ones, sorted by priority
        query = query.filter(Mission.energy_cost.in_([EnergyState.high_focus, EnergyState.neutral]))
    elif energy_state == EnergyState.low_focus:
        # Low focus: we only show low energy tasks
        query = query.filter(Mission.energy_cost == EnergyState.low_focus)
    else:
        # Neutral: neutral and low energy
        query = query.filter(Mission.energy_cost.in_([EnergyState.neutral, EnergyState.low_focus]))
        
    missions = query.order_by(Mission.base_priority.desc()).limit(10).all()
    
    return missions

from pydantic import BaseModel
from fastapi import HTTPException

class MissionCreate(BaseModel):
    title: str
    energy_cost: str = "neutral"

@router.post("/missions")
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    db_mission = Mission(
        title=mission.title,
        energy_cost=mission.energy_cost,
        status="pending"
    )
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

@router.put("/missions/{mission_id}/toggle")
def toggle_mission(mission_id: str, db: Session = Depends(get_db)):
    db_mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
        
    db_mission.status = "completed" if db_mission.status == "pending" else "pending"
    db.commit()
    return {"status": db_mission.status}
