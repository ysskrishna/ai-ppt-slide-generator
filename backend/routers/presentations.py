from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from core.dbutils import get_db
from models.models import Presentation
from models.schemas import PresentationCreate, PresentationOut, ConfigurationUpdate
from services.content_generator import generate_content_with_gemini
from services.pptx_generator import build_pptx

router = APIRouter()

@router.post("/", response_model=PresentationOut, summary="Create a new presentation")
def create_presentation(presentation: PresentationCreate, db: Session = Depends(get_db)):
    if presentation.custom_content:
        content = [slide.dict() for slide in presentation.custom_content]
        citations = "User provided custom content."
    else:
        content, citations = generate_content_with_gemini(presentation.topic)
    db_presentation = Presentation(
        title=presentation.topic,
        topic=presentation.topic,
        content=content,
        citations=citations
    )
    db.add(db_presentation)
    db.commit()
    db.refresh(db_presentation)
    return db_presentation

@router.post("/{id}/configure", response_model=PresentationOut, summary="Configure a presentation and generate PPTX")
def configure_presentation(id: int, config: ConfigurationUpdate, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.id == id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    presentation.configuration = config.dict()
    pptx_path = build_pptx(presentation.id, presentation.title, presentation.content, config.dict())
    presentation.pptx_path = pptx_path
    db.commit()
    db.refresh(presentation)
    return presentation

@router.get("/{id}", response_model=PresentationOut, summary="Get a presentation")
def get_presentation(id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.id == id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return presentation

@router.get("/{id}/download", summary="Download the generated PPTX")
def download_pptx(id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.id == id).first()
    if not presentation or not presentation.pptx_path:
        raise HTTPException(status_code=404, detail="PPTX not found")
    return FileResponse(path=presentation.pptx_path, filename=f"{presentation.title}.pptx", media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
