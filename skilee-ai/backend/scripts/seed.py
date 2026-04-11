from datetime import datetime, timedelta, timezone

from app.database import SessionLocal
from app.models import User, Subscription, Contract
from app.auth import hash_password


def get_or_create_user(db, email, role, password="password123"):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(email=email, role=role, password_hash=hash_password(password))
    db.add(user)
    db.flush()
    return user


def run_seed():
    db = SessionLocal()
    try:
        admin = get_or_create_user(db, "admin@skilee.ai", "admin")
        contractor = get_or_create_user(db, "contractor@skilee.ai", "contractor")
        trainer = get_or_create_user(db, "trainer@skilee.ai", "trainer")

        sub = db.query(Subscription).filter(Subscription.user_id == contractor.id).first()
        if not sub:
            db.add(
                Subscription(
                    user_id=contractor.id,
                    tier="premium",
                    start_date=datetime.now(timezone.utc),
                    end_date=datetime.now(timezone.utc) + timedelta(days=30),
                )
            )

        contract = db.query(Contract).filter(Contract.created_by == contractor.id).first()
        if not contract:
            db.add(
                Contract(
                    company_name="Skilee Labs",
                    title="Python & ML Bootcamp Trainer",
                    description="Need 3 trainers for Python and Machine Learning corporate upskilling.",
                    subject="Machine Learning",
                    required_trainers=3,
                    created_by=contractor.id,
                )
            )

        db.commit()
        print("Seed completed")
        print("Admin: admin@skilee.ai / password123")
        print("Contractor: contractor@skilee.ai / password123")
        print("Trainer: trainer@skilee.ai / password123")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
