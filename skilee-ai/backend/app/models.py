from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contracts = relationship("Contract", back_populates="creator")
    applications = relationship("Application", back_populates="trainer")
    subscription = relationship("Subscription", back_populates="user", uselist=False)


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    required_trainers = Column(Integer, nullable=False, default=2)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    creator = relationship("User", back_populates="contracts")
    applications = relationship("Application", back_populates="contract", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cover_letter = Column(Text, default="")
    cv_url = Column(String, nullable=False)
    cv_path = Column(String, nullable=False)
    skills = Column(String, default="")
    years_experience = Column(Integer, default=0)
    relevance_score = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contract = relationship("Contract", back_populates="applications")
    trainer = relationship("User", back_populates="applications")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    tier = Column(String, nullable=False, default="free")
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="subscription")
