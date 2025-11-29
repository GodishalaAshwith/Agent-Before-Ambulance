import google.generativeai as genai
import json

from utils import retry_with_backoff

class TriageAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.system_instruction = """
        You are a Triage Agent for a medical emergency system.
        Your goal is to:
        1. Identify the accident type (e.g., bleeding, unconscious, seizure, burns).
        2. Estimate the severity level (1-5), where 5 is most critical.
        3. Determine if an ambulance should be dispatched (Severity >= 3).
        
        Output JSON:
        {
            "accident_type": "string",
            "severity": int,
            "dispatch_ambulance": bool,
            "reasoning": "string"
        }
        """

    @retry_with_backoff(retries=2, initial_delay=0.5)
    def analyze(self, user_input: str) -> dict:
        prompt = f"{self.system_instruction}\n\nUser Input: {user_input}"
        response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return {
                "accident_type": "unknown",
                "severity": 0,
                "dispatch_ambulance": False,
                "reasoning": "Failed to parse response"
            }
