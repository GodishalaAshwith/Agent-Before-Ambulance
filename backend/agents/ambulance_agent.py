import google.generativeai as genai
import uuid
import random
import json
from tools.time_tool import get_current_time

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

    @retry_with_backoff(retries=2, initial_delay=0.5)
    def dispatch(self, injury_type: str, location: str = "Unknown location", history: list = None) -> dict:
        chat = self.model.start_chat(history=history or [])
        
        json_instruction = f"""
        Dispatch the ambulance for the given injury.
        You MUST use the `dispatch_ambulance` tool.
        
        Injury type: {injury_type}
        Location: {location}
        
        After dispatching, return a JSON object with:
        - "eta": The estimated time of arrival (integer minutes) returned by the tool.
        - "dispatch_id": The dispatch ID returned by the tool.
        
        If dispatch fails, return {{"eta": null, "dispatch_id": null}}.
        """
        
        response = chat.send_message(f"{self.system_instruction}\n{json_instruction}")
        
        # Check if function call is needed
        if response.parts[0].function_call:
            # Extract function call details
            function_call = response.parts[0].function_call
            function_name = function_call.name
            function_args = function_call.args
            
            if function_name == "dispatch_ambulance":
                # Call the tool
                tool_result = self.tools[0](**function_args)
                
                # Send the tool result back to the model
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={"result": tool_result}
                                )
                            )
                        ]
                    )
                )
        
        try:
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            result = json.loads(text)
            
            # Add timestamp from MCP tool
            time_data = get_current_time()
            result["timestamp"] = time_data["timestamp"]
            
            return result
        except Exception:
            # Attempt to extract from text if JSON parsing fails
            return {"eta": None, "dispatch_id": None, "raw_response": response.text}
