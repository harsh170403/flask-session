import time
import pytest
from app import SimpleSession  

@pytest.fixture
def session_manager():
    return SimpleSession()

def test_create_session(session_manager):
    session_id = session_manager.create_session()
    assert session_id is not None
    assert len(session_id) == 32  
    assert session_id in session_manager.sessions

def test_set_and_get_session_data(session_manager):
    session_id = session_manager.create_session()
    session_manager.set_session_data(session_id, 'username', 'john_doe')
    data = session_manager.get_session_data(session_id)
    assert data is not None
    assert data['username'] == 'john_doe'

def test_cleanup_sessions(session_manager):
    session_id = session_manager.create_session()
    session_manager.set_session_data(session_id, 'username', 'john_doe')

    time.sleep(2)
    session_manager.cleanup_sessions(timeout=1)
    
    assert session_id not in session_manager.sessions

def test_cleanup_sessions_no_deletion(session_manager):
    session_id = session_manager.create_session()
    session_manager.set_session_data(session_id, 'username', 'john_doe')

    session_manager.cleanup_sessions(timeout=10)
    
    assert session_id in session_manager.sessions

def test_get_nonexistent_session_data(session_manager):
    session_id = "nonexistent_session"
    data = session_manager.get_session_data(session_id)
    assert data is None
