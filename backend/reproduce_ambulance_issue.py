import os
from dotenv import load_dotenv
import google.generativeai as genai
from agents.ambulance_agent import AmbulanceAgent

# Load environment variables
load_dotenv()

# Configure GenAI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)

def test_ambulance_agent():
    print("Initializing AmbulanceAgent...")
    agent = AmbulanceAgent()
    
    # Test query that should trigger dispatch_ambulance
    user_input = "Dispatch to 123 Main St for severe bleeding"
    print(f"Sending query: {user_input}")
    
    try:
        response = agent.process(user_input)
        print("\nResponse received:")
        print(response)
        print("\nSUCCESS: Agent handled function call and returned text.")
    except Exception as e:
        print(f"\nFAILURE: Agent crashed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ambulance_agent()
