import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.database.dbmodels import Session, ConversationStep

# from .backend.routers.llms import generate_text  # Your LLM API call function

# Initialize session state
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

# Database connection
engine = create_engine('sqlite:///./AgentsDatabase.db')
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def create_new_session():
    """Create a new chat session"""
    # For demo, using user_id=1. In production, get from auth
    new_session = Session(
        user_id=1,
        title=f"New Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        planner_model_id="gpt-4",
        evaluator_model_id="gpt-3.5",
        is_active=True
    )
    db.add(new_session)
    db.commit()
    return new_session.session_id

def get_user_sessions():
    """Get all sessions for current user"""
    return db.query(Session).filter_by(user_id=1).order_by(desc(Session.created_at)).all()

def get_session_messages(session_id):
    """Get all messages for a session"""
    return db.query(ConversationStep).filter_by(session_id=session_id).order_by(ConversationStep.created_at).all()

# Sidebar
with st.sidebar:
    st.title("Chat Sessions")
    
    # New Chat button
    if st.button("+ New Chat"):
        st.session_state.current_session_id = create_new_session()
        st.rerun()
    
    # List of previous sessions
    sessions = get_user_sessions()
    for session in sessions:
        if st.button(
            f"{session.title}", 
            key=f"session_{session.session_id}",
            use_container_width=True,
            type="secondary" if session.session_id != st.session_state.current_session_id else "primary"
        ):
            st.session_state.current_session_id = session.session_id
            st.rerun()

# Main chat area
if st.session_state.current_session_id:
    # Get current session
    current_session = db.query(Session).get(st.session_state.current_session_id)
    st.header(current_session.title)
    
    # Display messages
    messages = get_session_messages(st.session_state.current_session_id)
    for msg in messages:
        if msg.step_type.value == "prompt":
            st.chat_message("user").write(msg.content)
        else:
            st.chat_message("assistant").write(msg.content)
    
    # Input prompt
    if prompt := st.chat_input("Enter your prompt..."):
        # Save user prompt
        new_prompt = ConversationStep(
            session_id=st.session_state.current_session_id,
            step_type="prompt",
            content=prompt
        )
        db.add(new_prompt)
        db.commit()
        
        # Generate and save response
        response = generate_response(prompt)  # Your LLM API call
        new_response = ConversationStep(
            session_id=st.session_state.current_session_id,
            step_type="plan",
            content=response,
            parent_step_id=new_prompt.step_id
        )
        db.add(new_response)
        db.commit()
        
        st.rerun()
else:
    st.info("Select a chat session or create a new one to start.")

# Ensure database connection is closed
db.close()