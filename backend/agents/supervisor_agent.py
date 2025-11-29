from typing import Dict, Any
from agents.triage_agent import TriageAgent
from agents.location_agent import LocationAgent
from agents.ambulance_agent import AmbulanceAgent
from agents.ambulance_agent import AmbulanceAgent
from agents.first_aid_agent import FirstAidAgent
from memory.session_service import InMemorySessionService

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
        Public entry point for FastAPI.
        Loads the session state, runs handle_message(), and saves updated state.
        """
        try:
            print(f"[DEBUG] Processing message for session {session_id}: {user_input}")
            state = InMemorySessionService.get_state(session_id)
            print(f"[DEBUG] Loaded state: {state}")

            result = await self.handle_message(user_input, state)
            print(f"[DEBUG] Result: {result}")

            InMemorySessionService.update_state(session_id, result["state"])

            return result["response"]
        except Exception as e:
            print(f"[ERROR] Exception in process_message: {e}")
            import traceback
            traceback.print_exc()
            return f"Error processing message: {str(e)}"

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

        # Check for severe injury keywords that should trigger re-triage
        severe_keywords = ["skull", "fracture", "unconscious", "not breathing", "severe bleeding", 
                          "chest pain", "heart attack", "stroke", "broken bone", "head injury"]
        should_retriage = any(keyword in user_input.lower() for keyword in severe_keywords)
        
        # If injury severity is not known yet OR severe keywords detected → (re)triage
        if state.get("severity") is None or (should_retriage and state.get("severity", 0) < 3):
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
        print(f"[DEBUG] Dispatching ambulance for {state['injury_type']}")
        location = state.get("location", {}).get("address", "Unknown location")
        dispatch_result = self.ambulance_agent.dispatch(
            injury_type=state["injury_type"],
            location=location
        )
        print(f"[DEBUG] Dispatch result: {dispatch_result}")

        state["ambulance_dispatched"] = True
        state["dispatch_eta"] = dispatch_result.get("eta")
        state["dispatch_id"] = dispatch_result.get("dispatch_id")
        state["dispatch_timestamp"] = dispatch_result.get("timestamp")

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
            
            response_text = f"I have your location: {loc['address']}."
            
            # If severity is high and ambulance not dispatched, dispatch NOW
            if state.get("severity", 0) >= 3 and not state.get("ambulance_dispatched"):
                # Actually dispatch the ambulance
                print(f"[DEBUG] Auto-dispatching ambulance after location provided")
                dispatch_result = self.ambulance_agent.dispatch(
                    injury_type=state["injury_type"],
                    location=loc.get("address", "Unknown location")
                )
                print(f"[DEBUG] Dispatch result: {dispatch_result}")
                
                state["ambulance_dispatched"] = True
                state["dispatch_eta"] = dispatch_result.get("eta")
                state["dispatch_id"] = dispatch_result.get("dispatch_id")
                state["dispatch_timestamp"] = dispatch_result.get("timestamp")
                
                response_text += f" Ambulance dispatched (ID: {state['dispatch_id']}). Estimated arrival time is {state['dispatch_eta']} minutes. Now let's focus on first aid."
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
