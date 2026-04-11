from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contract, Application, User
from ..schemas import ApplicationOut
from ..auth import require_roles
from ..storage import upload_cv, delete_cv
from ..ai_utils import analyze_cv

router = APIRouter(tags=["applications"])


@router.get("/applications/me", response_model=list[ApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("trainer")),
):
    return (
        db.query(Application)
        .filter(Application.trainer_id == user.id)
        .order_by(Application.created_at.desc())
        .all()
    )


@router.post("/contracts/{contract_id}/apply", response_model=ApplicationOut)
def apply_contract(
    contract_id: int,
    cover_letter: str = Form(""),
    skills: str = Form(""),
    years_experience: int = Form(0),
    cv: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("trainer")),
):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    existing = (
        db.query(Application)
        .filter(Application.contract_id == contract_id, Application.trainer_id == user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already applied")

    file_bytes = cv.file.read()
    path, url = upload_cv(file_bytes, cv.filename, user.id)
    relevance_score = analyze_cv(cv.filename, contract.subject, skills, years_experience)

    application = Application(
        contract_id=contract_id,
        trainer_id=user.id,
        cover_letter=cover_letter,
        cv_url=url,
        cv_path=path,
        skills=skills,
        years_experience=years_experience,
        relevance_score=relevance_score,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.put("/applications/{application_id}/cv", response_model=ApplicationOut)
def reupload_cv(
    application_id: int,
    skills: str = Form(""),
    years_experience: int = Form(0),
    cv: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("trainer")),
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.trainer_id != user.id:
        raise HTTPException(status_code=403, detail="Not your application")

    contract = db.query(Contract).filter(Contract.id == application.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract missing")

    old_path = application.cv_path
    file_bytes = cv.file.read()
    path, url = upload_cv(file_bytes, cv.filename, user.id)

    try:
        delete_cv(old_path)
    except Exception:
        pass

    application.cv_path = path
    application.cv_url = url
    application.skills = skills or application.skills
    application.years_experience = years_experience
    application.relevance_score = analyze_cv(cv.filename, contract.subject, application.skills, application.years_experience)

    db.commit()
    db.refresh(application)
    return application
