import google.generativeai as genai
from tools.geocode import reverse_geocode
import json

from utils import retry_with_backoff

class LocationAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.tools = [reverse_geocode]
        self.model = genai.GenerativeModel(model_name, tools=self.tools)
        self.system_instruction = """
        You are a Location Agent. Your job is to extract location information from the user's input and resolve it to a specific address using the `reverse_geocode` tool.
        
        If the user provides a location, use the tool to get the details.
        Return the final location details.
        """

    @retry_with_backoff(retries=3, initial_delay=2)
    def process(self, user_input: str, history: list = None):
        chat = self.model.start_chat(history=history or [])
        response = chat.send_message(f"{self.system_instruction}\n\nUser Input: {user_input}")
        
        # Check if function call is needed (handled automatically by GenAI lib usually, but we might need to invoke)
        # For simplicity in this mock, we assume the model uses the tool and returns the result.
        # In a real ADK loop, this would be handled by the runtime.
        
        # For this implementation, we'll return the text response.
        return response.text
