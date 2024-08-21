import os
import time

class SimpleSession:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = self._generate_session_id()
        self.sessions[session_id] = {
            'data': {},
            'created_at': time.time()
        }
        return session_id

    def get_session_data(self, session_id):
        return self.sessions.get(session_id, {}).get('data', None)

    def set_session_data(self, session_id, key, value):
        if session_id in self.sessions:
            self.sessions[session_id]['data'][key] = value

    def _generate_session_id(self):
        return os.urandom(16).hex()

    def cleanup_sessions(self, timeout=3600):
        current_time = time.time()
        to_delete = [sid for sid, sess in self.sessions.items() 
                     if current_time - sess['created_at'] > timeout]
        for sid in to_delete:
            del self.sessions[sid]

if __name__ == "__main__":
    session_manager = SimpleSession()

    session_id = session_manager.create_session()
    print(f"New session created: {session_id}")

    session_manager.set_session_data(session_id, 'username', 'john_doe')
    print("Session data set.")

    data = session_manager.get_session_data(session_id)
    print(f"Session data: {data}")

    session_manager.cleanup_sessions()
