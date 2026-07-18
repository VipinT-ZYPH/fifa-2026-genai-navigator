# FastAPI backend server
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_handler import generate_response

app = FastAPI(title="FIFA 2026 Stadium Navigator")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    user_location: str = "Main Gate"
    accessibility_needs: str = "None"

@app.post("/chat")
async def chat(request: QueryRequest):
    """Main chat endpoint"""
    try:
        response = generate_response(
            request.query,
            request.user_location,
            request.accessibility_needs
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def status():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "FIFA 2026 Stadium Navigator API",
        "version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    print("🏟️  Starting FIFA Stadium Navigator Backend...")
    print("Make sure Ollama is running: ollama serve")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)