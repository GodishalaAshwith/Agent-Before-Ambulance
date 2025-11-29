from typing import Dict, Any
from agents.triage_agent import TriageAgent
from agents.location_agent import LocationAgent
from agents.ambulance_agent import AmbulanceAgent
from agents.first_aid_agent import FirstAidAgent

class SupervisorAgent:
    """
    The Supervisor Agent orchestrates the entire emergency workflow.
    It routes user messages to specialized agents based on intent + context.
    """

    def __init__(self):
        self.triage_agent = TriageAgent()
        self.first_aid_agent = FirstAidAgent()
        self.location_agent = LocationAgent()
        self.ambulance_agent = AmbulanceAgent()
        
        # Internal state storage (session-specific)
        self.state = {
            "incident_started": False,
            "severity": None,
            "injury_type": None,
            "ambulance_dispatched": False,
            "dispatch_eta": None,
            "location": None,
            "step_index": 0,
            "history": []
        }

    async def process_message(self, user_input: str, session_id: str) -> str:
        """
        Wrapper to handle message processing and state management.
        """
        # In a real scenario with external session store, we would load state here using session_id
        # For now, self.state is the session state
        
        result = await self.handle_message(user_input, self.state)
        
        # Update state
        self.state = result["state"]
        
        return result["response"]

    # --------------------------------------------------------
    # MAIN ENTRY POINT
    # --------------------------------------------------------
    async def handle_message(self, user_input: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main orchestrator.
        Takes user input + session state → decides which agent to call.
        Returns: { "response": "...", "state": updated_state }
        """

        intent = self._detect_intent(user_input)

        # If no accident has started yet
        if not state.get("incident_started", False):
            return await self._start_incident(user_input, state)

        # If injury severity is not known yet → triage
        if state.get("severity") is None:
            return await self._run_triage(user_input, state)

        # If severity high but not dispatched → dispatch ambulance
        if state.get("severity", 0) >= 3 and not state.get("ambulance_dispatched", False):
            # Check if we have location
            if not state.get("location"):
                 return await self._run_location_agent(user_input, state)
            return await self._run_ambulance_dispatch(state)

        # If no location yet (and not already handled above)
        # Note: Logic slightly adjusted to ensure location is asked if needed for dispatch OR general record
        if not state.get("location") and state.get("severity", 0) >= 3:
             return await self._run_location_agent(user_input, state)

        # If we have injury + location (or low severity) → first aid steps
        return await self._run_first_aid(user_input, state)


    # --------------------------------------------------------
    # STAGE 1 — Start Incident
    # --------------------------------------------------------
    async def _start_incident(self, user_input: str, state: Dict[str, Any]):
        state["incident_started"] = True
        return {
            "response": "I understand. I’m here to help. Can you describe what happened?",
            "state": state,
        }

    # --------------------------------------------------------
    # STAGE 2 — TRIAGE (Assess Injury Severity)
    # --------------------------------------------------------
    async def _run_triage(self, user_input: str, state: Dict[str, Any]):
        # Note: calling sync method from async function
        triage_result = self.triage_agent.analyze(user_input)

        state["severity"] = triage_result["severity"]
        # Map accident_type to injury_type
        state["injury_type"] = triage_result.get("accident_type", "unknown")

        response = (
            f"Thanks. Based on your description, this seems like a {state['injury_type']} injury "
            f"with severity level {state['severity']}."
        )

        if state["severity"] >= 3:
            response += " This is serious. I may need to dispatch an ambulance."
            # Prompt for location immediately if serious
            if not state.get("location"):
                response += " Please provide your current location."

        return { "response": response, "state": state }

    # --------------------------------------------------------
    # STAGE 3 — DISPATCH AMBULANCE
    # --------------------------------------------------------
    async def _run_ambulance_dispatch(self, state: Dict[str, Any]):
        dispatch_result = self.ambulance_agent.dispatch(
            injury_type=state["injury_type"]
        )

        state["ambulance_dispatched"] = True
        state["dispatch_eta"] = dispatch_result.get("eta")
        state["dispatch_id"] = dispatch_result.get("dispatch_id")

        return {
            "response": f"Ambulance dispatched (ID: {state['dispatch_id']}). Estimated arrival time is {state['dispatch_eta']} minutes. Now let's focus on first aid.",
            "state": state,
        }

    # --------------------------------------------------------
    # STAGE 4 — LOCATION HANDLING
    # --------------------------------------------------------
    async def _run_location_agent(self, user_input: str, state: Dict[str, Any]):
        loc = self.location_agent.extract_location(user_input)

        if loc and loc.get("address"):
            state["location"] = loc
            
            # If we just got the location and severity is high, we might want to auto-dispatch next turn or now.
            # For this flow, we'll return response and let next turn handle dispatch if needed, 
            # OR we can recursively call dispatch here. 
            # Let's return response to keep it simple and interactive.
            
            response_text = f"I have your location: {loc['address']}."
            if state.get("severity", 0) >= 3 and not state.get("ambulance_dispatched"):
                 response_text += " I am dispatching an ambulance now."
                 # We could trigger dispatch here, but let's let the loop handle it next time or force a re-eval?
                 # To make it smooth, let's just acknowledge. The user will likely say "ok" or "help", triggering dispatch next.
                 # OR we can chain it.
                 # Let's chain it if we want immediate dispatch.
                 # But for now, let's stick to the requested flow.
            else:
                 response_text += " Now let's focus on first aid."

            return {
                "response": response_text,
                "state": state,
            }
        
        return {
            "response": "I need your location to guide the ambulance. Please describe where you are.",
            "state": state,
        }

    # --------------------------------------------------------
    # STAGE 5 — FIRST AID GUIDANCE
    # --------------------------------------------------------
    async def _run_first_aid(self, user_input: str, state: Dict[str, Any]):
        step_result = self.first_aid_agent.get_next_step(
            injury_type=state["injury_type"],
            step_index=state.get("step_index", 0),
            user_input=user_input
        )

        state["step_index"] = step_result["next_step_index"]
        
        response = step_result["instruction"]
        if step_result.get("completed"):
            response += "\n\nYou have completed the first aid steps. Help should be arriving soon."

        return {
            "response": response,
            "state": state
        }

    # --------------------------------------------------------
    # INTENT DETECTION (Placeholder)
    # --------------------------------------------------------
    def _detect_intent(self, text: str):
        text_lower = text.lower()

        if any(word in text_lower for word in ["accident", "injured", "hurt", "bleeding"]):
            return "DESCRIBE_INJURY"
        if any(word in text_lower for word in ["near", "at", "close to", "location"]):
            return "PROVIDE_LOCATION"
        if any(word in text_lower for word in ["what do i do", "help", "what next"]):
            return "REQUEST_FIRST_AID"
        if text_lower in ["stop", "end", "bye"]:
            return "END_SESSION"

        return "UNSPECIFIED"
