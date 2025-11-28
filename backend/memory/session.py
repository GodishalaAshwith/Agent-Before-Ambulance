from agents.supervisor_agent import SupervisorAgent
import uuid

class InMemorySessionService:
    def __init__(self):
        self.sessions = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SupervisorAgent()
        return session_id

    def get_agent(self, session_id: str) -> SupervisorAgent:
        return self.sessions.get(session_id)
