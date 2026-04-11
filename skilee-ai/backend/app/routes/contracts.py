from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contract, Application, Subscription, User
from ..schemas import ContractCreate, ContractOut, ApplicationsTierResponse
from ..auth import get_current_user, require_roles
from ..ai_utils import parse_contract_description

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.post("", response_model=ContractOut)
def create_contract(
    payload: ContractCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("contractor")),
):
    parsed = parse_contract_description(payload.description)
    contract = Contract(
        company_name=payload.company_name,
        description=payload.description,
        title=payload.title,
        subject=parsed["subject"],
        required_trainers=parsed["required_trainers"],
        created_by=user.id,
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


@router.get("", response_model=list[ContractOut])
def list_contracts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role == "contractor":
        return db.query(Contract).filter(Contract.created_by == user.id).order_by(Contract.created_at.desc()).all()
    return db.query(Contract).order_by(Contract.created_at.desc()).all()


@router.get("/{contract_id}/applications", response_model=ApplicationsTierResponse)
def get_contract_applications(
    contract_id: int,
    tier: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("contractor", "admin")),
):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if user.role == "contractor" and contract.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not your contract")

    effective_tier = tier
    if not effective_tier:
        if user.role == "admin":
            effective_tier = "premium"
        else:
            sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
            effective_tier = sub.tier if sub else "free"

    applicants = (
        db.query(Application)
        .filter(Application.contract_id == contract_id)
        .order_by(Application.relevance_score.desc(), Application.created_at.desc())
        .all()
    )

    if effective_tier == "free":
        return {"tier": "free", "applicant_count": len(applicants), "applicants": None}

    if effective_tier == "standard":
        return {"tier": "standard", "applicant_count": len(applicants), "applicants": applicants}

    shortlist_count = contract.required_trainers * 2
    return {
        "tier": "premium",
        "applicant_count": len(applicants),
        "applicants": applicants[:shortlist_count],
    }
