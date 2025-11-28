import os
import traceback
import google.generativeai as genai

# Mock API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyD-mock-key"

def test_triage():
    print("Testing TriageAgent...")
    try:
        from agents.triage_agent import TriageAgent
        agent = TriageAgent()
        print("TriageAgent init ok")
    except:
        traceback.print_exc()

def test_location():
    print("\nTesting LocationAgent...")
    try:
        from agents.location_agent import LocationAgent
        agent = LocationAgent()
        print("LocationAgent init ok")
    except:
        traceback.print_exc()

test_triage()
test_location()
