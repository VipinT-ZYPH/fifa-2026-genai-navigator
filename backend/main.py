# FastAPI backend server
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
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

@app.post("/chat")
async def chat(request: dict):
    """Main chat endpoint"""
    try:
        query = request.get("query", "").strip()
        user_location = request.get("user_location", "Main Gate").strip()
        accessibility_needs = request.get("accessibility_needs", "None").strip()
        
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        response = generate_response(query, user_location, accessibility_needs)
        return response
    except Exception as e:
        return {"error": str(e), "response": "Error processing request"}

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
    port = int(os.getenv("PORT", 8000))
    print("🏟️  Starting FIFA Stadium Navigator Backend...")
    uvicorn.run(app, host="0.0.0.0", port=port)