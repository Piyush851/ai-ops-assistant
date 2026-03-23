# The entry point that ties the user input to the 3-agent flow# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from api.routes import router as api_router  <-- We will connect this later

app = FastAPI(title="AI Ops Assistant API")

# Infrastructure: Enable CORS so your React frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # React/Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def process_chat(request: ChatRequest):
    """
    This is where your frontend will send the user's message.
    Later, we will wire this up to trigger the Planner -> Executor -> Verifier flow.
    """
    user_message = request.prompt
    
    # TODO: Pass user_message to the Planner Agent
    
    return {
        "status": "success",
        "response": f"Received: '{user_message}'. The agents are currently sleeping!",
        "agent_logs": ["Planner started...", "Tools executed...", "Verifier approved."]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)