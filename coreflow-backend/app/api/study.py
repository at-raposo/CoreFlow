from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.taxonomy import Topic, Tag, topic_tags

router = APIRouter()

@router.post("/toggle/{topic_id}")
def study_toggle(topic_id: str, db: Session = Depends(get_db)):
    """
    Toggle Topic Progress: Marks/Unmarks a topic ONLY. 
    (Propagation disabled as per user request for manual control).
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Tópico não encontrado")

    # Toggle the state
    new_state = not topic.is_completed
    topic.is_completed = new_state
    topic.knowledge_level = 100 if new_state else 0
    
    db.commit()
    
    return {
        "message": "Progresso atualizado!",
        "is_completed": topic.is_completed,
        "intersection_count": 0
    }
