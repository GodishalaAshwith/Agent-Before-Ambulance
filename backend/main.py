from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from memory.session import InMemorySessionService
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

class MessageRequest(BaseModel):
    session_id: str
    message: str

class MessageResponse(BaseModel):
    text: str
    end: bool = False

@app.post("/new-session")
async def new_session():
    session_id = session_service.create_session()
    return {"session_id": session_id}

@app.post("/agent", response_model=MessageResponse)
async def agent_chat(request: MessageRequest):
    agent = session_service.get_agent(request.session_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # process_message is now async
    response_text = await agent.process_message(request.message, request.session_id)
    return {"text": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
