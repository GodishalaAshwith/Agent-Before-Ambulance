import google.generativeai as genai

import json
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
    def get_next_step(self, injury_type: str, step_index: int, user_input: str, history: list = None) -> dict:
        chat = self.model.start_chat(history=history or [])
        
        json_instruction = f"""
        Provide the next first aid step for: {injury_type}.
        Current step index: {step_index}.
        
        Return a JSON object with:
        - "instruction": The text instruction for the user.
        - "next_step_index": The index for the next step (increment by 1).
        - "completed": Boolean, true if all steps are finished.
        """
        
        prompt = f"{self.system_instruction}\n{json_instruction}\n\nUser Input: {user_input}"
        response = chat.send_message(prompt)
        
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            return json.loads(text)
        except Exception:
            return {
                "instruction": response.text,
                "next_step_index": step_index + 1,
                "completed": False
            }
