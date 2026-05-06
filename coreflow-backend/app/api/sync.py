from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.jupiter_scraper import fetch_usp_syllabus
from app.services.qc_scraper import fetch_qconcursos_stats
from app.models.taxonomy import Discipline, Topic

router = APIRouter()

@router.post("/jupiter")
def sync_jupiter_syllabus(course_code: str, db: Session = Depends(get_db)):
    """
    Fetches the syllabus from JupiterWeb and saves the topics in the database.
    """
    topics = fetch_usp_syllabus(course_code)
    
    if not topics:
        raise HTTPException(status_code=404, detail="Não foi possível extrair a ementa. Verifique o código da disciplina.")
        
    # Check if discipline exists, otherwise create it
    discipline = db.query(Discipline).filter(Discipline.name == course_code).first()
    if not discipline:
        discipline = Discipline(name=course_code)
        db.add(discipline)
        db.commit()
        db.refresh(discipline)
        
    # Create a generic Subject to hold these topics
    from app.models.taxonomy import Subject
    subject = db.query(Subject).filter(Subject.discipline_id == discipline.id).first()
    if not subject:
        subject = Subject(name="Ementa USP", discipline_id=discipline.id)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        
    # Add topics
    added_topics = []
    for t in topics:
        topic_obj = Topic(name=t[:250], subject_id=subject.id)
        db.add(topic_obj)
        added_topics.append(topic_obj)
        
    db.commit()
    return {"message": f"Extraídos {len(topics)} tópicos para {course_code}", "topics": topics}

@router.get("/qc/stats")
def sync_qconcursos_stats():
    """
    Fetches the user's statistics from QConcursos using Playwright.
    """
    stats = fetch_qconcursos_stats()
    if "error" in stats:
        raise HTTPException(status_code=401, detail=stats["error"])
    return stats
