import google.generativeai as genai
import uuid
import random

# Mock implementation of the tool for the agent to use directly
def dispatch_ambulance(location: str, injury: str):
    """
    Dispatches an ambulance to the specified location.
    
    Args:
        location: The location to dispatch to.
        injury: The description of the injury.
        
    Returns:
        A dictionary with ETA and dispatch ID.
    """
    return {
        "eta": random.randint(5, 15),
        "dispatch_id": str(uuid.uuid4())
    }

from utils import retry_with_backoff

class AmbulanceAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.tools = [dispatch_ambulance]
        self.model = genai.GenerativeModel(model_name, tools=self.tools)
        self.system_instruction = """
        You are an Ambulance Dispatch Agent.
        Your role is to dispatch an ambulance using the `dispatch_ambulance` tool.
        You need the 'location' and 'injury' details.
        Once dispatched, inform the user of the ETA and dispatch ID.
        """

    @retry_with_backoff(retries=3, initial_delay=2)
    def process(self, user_input: str, history: list = None):
        chat = self.model.start_chat(history=history or [])
        response = chat.send_message(f"{self.system_instruction}\n\nUser Input: {user_input}")
        return response.text
