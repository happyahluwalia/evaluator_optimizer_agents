from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, JSON, Enum, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import enum

Base = declarative_base()

class ModelType(enum.Enum):
    PLANNER = "planner"
    EVALUATOR = "evaluator"

class StepType(enum.Enum):
    PROMPT = "prompt"
    PLAN = "plan"
    EVALUATION = "evaluation"
    USER_FEEDBACK = "user_feedback"

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("Session", back_populates="user")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_email', email),  # For login lookups
        Index('idx_user_username', username),  # For username searches
    )

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    planner_model_id = Column(String(100), nullable=False)
    evaluator_model_id = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    conversation_steps = relationship("ConversationStep", back_populates="session")
    
    # Indexes
    __table_args__ = (
        Index('idx_session_user_created', user_id, created_at.desc()),  # For listing user's sessions by date
        Index('idx_session_active_user', user_id, is_active),  # For filtering active sessions
        Index('idx_session_title', title),  # For session search by title
    )

class ConversationStep(Base):
    __tablename__ = 'conversation_steps'
    
    step_id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.session_id'), nullable=False)
    step_type = Column(Enum(StepType), nullable=False)
    content = Column(Text, nullable=False)
    coversationmetadata = Column(JSON)
    parent_step_id = Column(Integer, ForeignKey('conversation_steps.step_id'), nullable=True)
    iteration = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="conversation_steps")
    children = relationship("ConversationStep",
                          backref=backref("parent", remote_side=[step_id]),
                          cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        # For retrieving conversation history
        Index('idx_conversation_session_created', session_id, created_at),
        
        # For tracking conversation flow
        Index('idx_conversation_parent_created', parent_step_id, created_at),
        
        # For filtering by step type within a session
        Index('idx_conversation_session_type', session_id, step_type),
        
        # For finding latest iteration in a session
        Index('idx_conversation_session_iteration', session_id, iteration.desc()),
        
        # For complex queries involving parent relationships
        Index('idx_conversation_session_parent_type', 
              session_id, parent_step_id, step_type)
    )

class ModelConfig(Base):
    __tablename__ = 'model_configs'
    
    model_id = Column(String(100), primary_key=True)
    model_type = Column(Enum(ModelType), nullable=False)
    description = Column(Text)
    configuration = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_model_type_active', model_type, is_active),  # For filtering active models by type
    )

# Helper functions for database operations
def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

def get_session_history(db_session, session_id):
    """Get complete conversation history for a session ordered by creation time"""
    return db_session.query(ConversationStep)\
        .filter(ConversationStep.session_id == session_id)\
        .order_by(ConversationStep.created_at)\
        .all()

def get_latest_iteration(db_session, session_id):
    """Get the latest iteration number for a session"""
    return db_session.query(ConversationStep)\
        .filter(ConversationStep.session_id == session_id)\
        .order_by(ConversationStep.iteration.desc())\
        .first()

def get_user_active_sessions(db_session, user_id):
    """Get all active sessions for a user ordered by last update"""
    return db_session.query(Session)\
        .filter(Session.user_id == user_id, Session.is_active == True)\
        .order_by(Session.updated_at.desc())\
        .all()