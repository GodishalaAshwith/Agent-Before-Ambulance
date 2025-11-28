import google.generativeai as genai
from agents.triage_agent import TriageAgent
from agents.location_agent import LocationAgent
from agents.ambulance_agent import AmbulanceAgent
from agents.first_aid_agent import FirstAidAgent

class SupervisorAgent:
    def __init__(self):
        self.triage_agent = TriageAgent()
        self.location_agent = LocationAgent()
        self.ambulance_agent = AmbulanceAgent()
        self.first_aid_agent = FirstAidAgent()
        
        # Simple in-memory state
        self.state = {
            "stage": "triage", # triage, location, dispatch, guidance
            "injury": None,
            "severity": 0,
            "location": None,
            "dispatch_info": None,
            "history": []
        }

    def process_message(self, user_input: str, session_id: str):
        # In a real app, load state from session_id
        
        response_text = ""
        
        if self.state["stage"] == "triage":
            triage_result = self.triage_agent.analyze(user_input)
            self.state["injury"] = triage_result.get("accident_type")
            self.state["severity"] = triage_result.get("severity")
            
            if triage_result.get("dispatch_ambulance"):
                self.state["stage"] = "location"
                response_text = f"I understand. This sounds serious ({self.state['injury']}). I need to dispatch an ambulance. What is your current location?"
            else:
                self.state["stage"] = "guidance"
                response_text = f"I see. It seems to be a {self.state['injury']}. Let's walk through some first aid steps."
                # Immediately get first step
                step = self.first_aid_agent.get_guidance(self.state["injury"], self.state["history"])
                response_text += f"\n\n{step}"

        elif self.state["stage"] == "location":
            # Assume user is providing location
            loc_response = self.location_agent.process(user_input)
            self.state["location"] = loc_response # Simplified
            
            self.state["stage"] = "dispatch"
            # Auto-proceed to dispatch
            dispatch_response = self.ambulance_agent.process(f"Dispatch to {self.state['location']} for {self.state['injury']}")
            self.state["dispatch_info"] = dispatch_response
            
            self.state["stage"] = "guidance"
            response_text = f"{dispatch_response}\n\nWhile help is on the way, let's do some first aid. {self.first_aid_agent.get_guidance(self.state['injury'], self.state['history'])}"

        elif self.state["stage"] == "guidance":
            response_text = self.first_aid_agent.get_guidance(self.state["injury"], self.state["history"])
            
        self.state["history"].append({"role": "user", "parts": [user_input]})
        self.state["history"].append({"role": "model", "parts": [response_text]})
        
        return response_text
