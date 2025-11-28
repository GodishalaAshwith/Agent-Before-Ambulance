import google.generativeai as genai

from utils import retry_with_backoff

class FirstAidAgent:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model_name)
        self.system_instruction = """
        You are a First Aid Guidance Agent.
        Your goal is to provide clear, step-by-step first aid instructions based on the injury.
        
        Rules:
        1. Give ONE step at a time.
        2. Wait for user confirmation or questions before moving to the next step.
        3. Be calm and reassuring.
        4. If the situation is critical (CPR needed), be very direct.
        """

    @retry_with_backoff(retries=3, initial_delay=2)
    def get_guidance(self, injury: str, history: list = None):
        chat = self.model.start_chat(history=history or [])
        prompt = f"{self.system_instruction}\n\nThe user has the following injury/situation: {injury}. Provide the next step."
        response = chat.send_message(prompt)
        return response.text
