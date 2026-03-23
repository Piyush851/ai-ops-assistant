# The entry point that ties the user input to the 3-agent flow# main.py
# main.py (Infrastructure Update)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from pydantic import BaseModel


app = FastAPI(title="AI Ops Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this to your React port in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Receive message from React
            user_message = await websocket.receive_text()
            
            # 2. Stream Status 1: Planner
            await websocket.send_json({"type": "status", "message": "🧠 Planner Agent is analyzing the request..."})
            await asyncio.sleep(1) # Simulating your partner's LLM delay
            
            # 3. Stream Status 2: Executor
            await websocket.send_json({"type": "status", "message": "⚙️ Executor Agent is fetching data from APIs..."})
            await asyncio.sleep(2) # Simulating API calls
            
            # 4. Stream Status 3: Verifier
            await websocket.send_json({"type": "status", "message": "✅ Verifier Agent is checking the output..."})
            await asyncio.sleep(1)
            
            # 5. Send Final Output (Your partner will replace this mock data with real JSON)
            mock_final_response = {
                "type": "result",
                "message": "Here is the data I found for you.",
                "data_type": "weather", # or "github"
                "payload": {"temperature": "28°C", "wind_speed": "12 km/h"}
            }
            await websocket.send_json(mock_final_response)

    except WebSocketDisconnect:
        print("Client disconnected")
        
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