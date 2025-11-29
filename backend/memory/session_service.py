class InMemorySessionService:
    """
    Minimal in-memory session manager.
    Stores session-specific state for each user.
    """
    _sessions = {}

    @classmethod
    def get_state(cls, session_id: str) -> dict:
        return cls._sessions.setdefault(session_id, {})

    @classmethod
    def update_state(cls, session_id: str, state: dict):
        cls._sessions[session_id] = state
