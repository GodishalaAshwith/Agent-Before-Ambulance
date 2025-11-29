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
        
        # Check if function call is needed
        if response.parts[0].function_call:
            # Extract function call details
            function_call = response.parts[0].function_call
            function_name = function_call.name
            function_args = function_call.args
            
            if function_name == "reverse_geocode":
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
                
        return response.text
