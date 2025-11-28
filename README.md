# Agent Before Ambulance

A multi-agent AI system designed to assist in medical emergencies before an ambulance arrives.

## Features
- **Voice Interface**: Speak to the agent directly.
- **Triage**: Automatically assesses injury severity.
- **First Aid Guidance**: Step-by-step instructions (CPR, bleeding control, etc.).
- **Ambulance Dispatch**: Simulates dispatching help to your location.
- **Location Services**: Integrated geocoding.

## Architecture
- **Frontend**: HTML/JS with Web Speech API.
- **Backend**: FastAPI with Google ADK Agents.

## Setup
1. Install dependencies: `pip install -r backend/requirements.txt`
2. Run backend: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8001`
3. Open `frontend/index.html` in your browser.
