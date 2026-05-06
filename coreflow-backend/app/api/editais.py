import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.taxonomy import Edital, Topic, Tag

class ParseCargoRequest(BaseModel):
    file_path: str
    cargo_name: str
from app.models.taxonomy import Edital, Topic

router = APIRouter()

@router.post("/extract-cargos")
async def extract_cargos(file: UploadFile = File(...)):
    """
    Receives a PDF edital, extracts its text, and returns a list of available Cargos.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Somente arquivos PDF são permitidos.")
        
    temp_dir = tempfile.gettempdir()
    temp_pdf_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_pdf_path, "wb") as f:
        f.write(await file.read())
        
    try:
        from app.services.edital_parser import extract_text_from_pdf, extract_cargos_from_text
        text_content = extract_text_from_pdf(temp_pdf_path)
        
        temp_txt_path = temp_pdf_path + ".txt"
        with open(temp_txt_path, "w", encoding="utf-8") as f:
            f.write(text_content)
            
        cargos = extract_cargos_from_text(text_content)
        
        return {
            "file_path": temp_txt_path,
            "cargos": cargos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse-cargo")
def parse_cargo(req: ParseCargoRequest, db: Session = Depends(get_db)):
    """
    Receives the selected cargo and the saved text file path, then generates the Skill Tree.
    """
    if not os.path.exists(req.file_path):
        raise HTTPException(status_code=400, detail="Arquivo temporário não encontrado.")
        
    with open(req.file_path, "r", encoding="utf-8") as f:
        text_content = f.read()
        
    from app.services.edital_parser import extract_syllabus_for_cargo
    
    try:
        parsed_data = extract_syllabus_for_cargo(text_content, req.cargo_name)
        
        title = parsed_data.get("title", req.cargo_name)
        topics = parsed_data.get("topics", [])
        
        if not topics:
            raise HTTPException(status_code=400, detail="Não foi possível extrair tópicos deste cargo.")
            
        edital = Edital(title=title)
        db.add(edital)
        db.commit()
        db.refresh(edital)
        
        for t_obj in topics:
            topic_name = t_obj.get("name", "Sem Nome")[:250]
            topic_tags = t_obj.get("tags", [])
            
            topic = Topic(name=topic_name)
            
            for tag_name in topic_tags:
                tag_name = tag_name.lower().strip()
                if not tag_name: continue
                
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name[:100])
                    db.add(tag)
                    db.flush()
                
                topic.tags.append(tag)
                
            edital.topics.append(topic)
            db.add(topic)
            
        db.commit()
        
        return {
            "message": "Skill Tree gerada com sucesso",
            "edital_id": edital.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_editais(db: Session = Depends(get_db)):
    editais = db.query(Edital).all()
    
    result = []
    for e in editais:
        total = len(e.topics)
        completed = sum(1 for t in e.topics if t.is_completed)
        progress = (completed / total * 100) if total > 0 else 0
        
        result.append({
            "id": e.id,
            "title": e.title,
            "status": e.status,
            "progress": round(progress),
            "total_topics": total
        })
        
    return result

@router.get("/{edital_id}")
def get_edital(edital_id: str, db: Session = Depends(get_db)):
    edital = db.query(Edital).filter(Edital.id == edital_id).first()
    if not edital:
        raise HTTPException(status_code=404, detail="Edital não encontrado")
        
    topics = []
    for t in edital.topics:
        topics.append({
            "id": t.id,
            "name": t.name,
            "knowledge_level": t.knowledge_level,
            "is_completed": t.is_completed,
            "tags": [tag.name for tag in t.tags]
        })
        
    return {
        "id": edital.id,
        "title": edital.title,
        "status": edital.status,
        "topics": topics
    }

@router.delete("/{edital_id}")
def delete_edital(edital_id: str, db: Session = Depends(get_db)):
    edital = db.query(Edital).filter(Edital.id == edital_id).first()
    if not edital:
        raise HTTPException(status_code=404, detail="Edital não encontrado")
        
    db.delete(edital)
    db.commit()
    return {"message": "Edital deletado com sucesso"}
