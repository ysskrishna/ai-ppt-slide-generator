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
    else:
        content = generate_content_with_gemini(presentation.topic, presentation.num_slides)
    db_presentation = Presentation(
        topic=presentation.topic,
        content=content
    )
    db.add(db_presentation)
    db.commit()
    db.refresh(db_presentation)
    return db_presentation

@router.post("/{presentation_id}/configure", response_model=PresentationOut, summary="Configure a presentation")
def configure_presentation(presentation_id: int, config: ConfigurationUpdate, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.presentation_id == presentation_id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    presentation.configuration = config.dict()
    db.commit()
    db.refresh(presentation)
    return presentation

@router.get("/{presentation_id}", response_model=PresentationOut, summary="Get a presentation")
def get_presentation(presentation_id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.presentation_id == presentation_id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    return presentation

@router.get("/{presentation_id}/download", summary="Download the generated PPTX")
def download_pptx(presentation_id: int, db: Session = Depends(get_db)):
    presentation = db.query(Presentation).filter(Presentation.presentation_id == presentation_id).first()
    if not presentation:
        raise HTTPException(status_code=404, detail="Presentation not found")
    
    # Generate PPTX with current configuration
    config = presentation.configuration or {}  # Use empty dict if no configuration
    pptx_path = build_pptx(presentation.presentation_id, presentation.content, config)
    presentation.pptx_path = pptx_path
    db.commit()
    
    return FileResponse(path=pptx_path, filename=f"presentation_{presentation.presentation_id}.pptx", media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
