import asyncio
import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
print(f"Adding to sys.path: {backend_path}")
sys.path.append(backend_path)

# Load env
load_dotenv(os.path.join(backend_path, ".env"))
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"Configuring GenAI with key: {api_key[:5]}...")
    genai.configure(api_key=api_key)
else:
    print("WARNING: No GOOGLE_API_KEY found.")

try:
    print("Importing AmbulanceAgent...")
    from agents.ambulance_agent import AmbulanceAgent
    print("Importing SupervisorAgent...")
    from agents.supervisor_agent import SupervisorAgent
    print("Importing InMemorySessionService...")
    from memory.session_service import InMemorySessionService
    print("Imports successful.")
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

async def verify_mcp_tool():
    print("\n--- Verifying MCP Tool Integration ---")
    print("Initializing AmbulanceAgent...")
    try:
        agent = AmbulanceAgent()
        print("AmbulanceAgent initialized.")
    except Exception as e:
        print(f"Error initializing AmbulanceAgent: {e}")
        return

    print("Calling get_current_time directly...")
    try:
        from tools.time_tool import get_current_time
        time_data = get_current_time()
        print(f"Direct Tool Call Result: {time_data}")
        if "timestamp" in time_data:
            print("PASS: get_current_time returns timestamp")
        else:
            print("FAIL: get_current_time missing timestamp")
    except Exception as e:
        print(f"Error calling tool: {e}")

async def verify_session_service():
    print("\n--- Verifying Session Service ---")
    session_id = "test_session_123"
    state = {"foo": "bar"}
    
    print("Updating state...")
    InMemorySessionService.update_state(session_id, state)
    print("Retrieving state...")
    retrieved = InMemorySessionService.get_state(session_id)
    
    if retrieved == state:
        print("PASS: Session state stored and retrieved correctly")
    else:
        print(f"FAIL: Session state mismatch. Expected {state}, got {retrieved}")

async def verify_supervisor():
    print("\n--- Verifying Supervisor Agent ---")
    print("Initializing SupervisorAgent...")
    supervisor = SupervisorAgent()
    session_id = "sup_test_session"
    
    print("Getting initial state...")
    initial_state = InMemorySessionService.get_state(session_id)
    print(f"Initial State: {initial_state}")
    
    # Mocking triage agent
    print("Mocking triage agent...")
    supervisor.triage_agent.analyze = lambda x: {"severity": 1, "accident_type": "minor cut"}
    
    print("Processing message...")
    try:
        response = await supervisor.process_message("I cut my finger", session_id)
        print(f"Response: {response}")
        
        updated_state = InMemorySessionService.get_state(session_id)
        print(f"Updated State: {updated_state}")
        
        if updated_state.get("incident_started"):
            print("PASS: Supervisor updated session state")
        else:
            print("FAIL: Supervisor did not update session state")
    except Exception as e:
        print(f"Error in process_message: {e}")
        import traceback
        traceback.print_exc()

async def main():
    print("Starting verification...")
    await verify_mcp_tool()
    await verify_session_service()
    await verify_supervisor()
    print("Verification finished.")

if __name__ == "__main__":
    asyncio.run(main())
