from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)  # Store hashed passwords
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    chat_session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    chat_session_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    user = relationship("User", back_populates="chat_sessions")

class Prompt(Base):
    __tablename__ = 'prompts'
    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.chat_session_id'), nullable=False)
    prompt_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="prompts")

class Plan(Base):
    __tablename__ = 'plans'
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    prompt_id = Column(Integer, ForeignKey('prompts.prompt_id'), nullable=False)
    model_id = Column(Integer, nullable=False)  # Reference model ID from config
    plan_text = Column(Text, nullable=False)
    iteration = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    prompt = relationship("Prompt", back_populates="plans")

class Evaluation(Base):
    __tablename__ = 'evaluations'
    evaluation_id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey('plans.plan_id'), nullable=False)
    model_id = Column(Integer, nullable=False)  # Reference model ID from config
    evaluation_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    plan = relationship("Plan", back_populates="evaluations")

class Discussion(Base):
    __tablename__ = 'discussions'
    discussion_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.chat_session_id'), nullable=False)
    step_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    session = relationship("Session", back_populates="discussions")
    __table_args__ = (
        CheckConstraint("step_type IN ('prompt', 'plan', 'evaluation')", name="check_step_type"),
    )

# Relationships
User.chatsessions = relationship("ChatSession", order_by=ChatSession.created_at, back_populates="user")
ChatSession.prompts = relationship("Prompt", order_by=Prompt.created_at, back_populates="chatsession")
Prompt.plans = relationship("Plan", order_by=Plan.created_at, back_populates="prompt")
Plan.evaluations = relationship("Evaluation", order_by=Evaluation.created_at, back_populates="plan")
ChatSession.discussions = relationship("Discussion", order_by=Discussion.created_at, back_populates="chatsession")
