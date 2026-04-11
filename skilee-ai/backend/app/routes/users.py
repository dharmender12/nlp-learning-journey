from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Contract, Application, Subscription
from ..schemas import SubscriptionUpdate, SubscriptionOut, AdminStats
from ..auth import get_current_user, require_roles

router = APIRouter(prefix="/users", tags=["users"])

TIER_PRICE = {
    "free": 0,
    "standard": 199,
    "premium": 249,
}


@router.post("/subscription", response_model=SubscriptionOut)
def update_subscription(
    payload: SubscriptionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("contractor")),
):
    tier = payload.tier.lower()
    if tier not in TIER_PRICE:
        raise HTTPException(status_code=400, detail="Invalid tier")

    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    now = datetime.now(timezone.utc)

    if not sub:
        sub = Subscription(user_id=user.id, tier=tier, start_date=now, end_date=now + timedelta(days=30))
        db.add(sub)
    else:
        sub.tier = tier
        sub.start_date = now
        sub.end_date = now + timedelta(days=30)

    db.commit()
    db.refresh(sub)
    return sub


@router.get("/me/subscription", response_model=SubscriptionOut)
def get_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("contractor")),
):
    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    if not sub:
        sub = Subscription(user_id=user.id, tier="free")
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return sub


@router.get("/admin/stats", response_model=AdminStats)
def admin_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_roles("admin")),
):
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_contracts = db.query(func.count(Contract.id)).scalar() or 0
    total_applications = db.query(func.count(Application.id)).scalar() or 0

    active_paid = (
        db.query(Subscription)
        .filter(Subscription.tier.in_(["standard", "premium"]))
        .all()
    )
    revenue = sum(TIER_PRICE.get(item.tier, 0) for item in active_paid)

    return {
        "total_users": int(total_users),
        "total_contracts": int(total_contracts),
        "total_applications": int(total_applications),
        "revenue_inr": int(revenue),
    }


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at,
    }
