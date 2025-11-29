from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from memory.session import InMemorySessionService
from agents.supervisor_agent import SupervisorAgent
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Explicitly configure GenAI
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("WARNING: GOOGLE_API_KEY not found in environment variables!")
else:
    print(f"GOOGLE_API_KEY found: {api_key[:5]}...")
    genai.configure(api_key=api_key)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()
supervisor = SupervisorAgent()

class MessageRequest(BaseModel):
    session_id: str
    message: str

class UserMessage(BaseModel):
    session_id: str
    message: str

class MessageResponse(BaseModel):
    text: str
    end: bool = False

@app.post("/new-session")
async def new_session():
    session_id = session_service.create_session()
    return {"session_id": session_id}

@app.post("/agent")
async def agent_chat(payload: UserMessage):
    response = await supervisor.process_message(
        payload.message,
        payload.session_id
    )
    return {"text": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
