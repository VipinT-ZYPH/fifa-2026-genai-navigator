# AI integration with Groq API
import requests
import os
from stadium_data import (
    get_closest_facility,
    get_crowd_status,
    get_accessible_routes,
    STADIUM_DATA
)

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def build_context(user_query: str, user_location: str, accessibility_needs: str) -> str:
    """Build context for AI model"""
    crowd_status = get_crowd_status()
    
    context = f"""You are a FIFA 2026 Stadium Assistant. Help fans navigate the stadium.
    
Stadium Status:
- Total capacity: 80,000
- Current crowd density: Zone A: {crowd_status['A']}%, Zone B: {crowd_status['B']}%, Zone C: {crowd_status['C']}%, Zone D: {crowd_status['D']}%

User Info:
- Current Location: {user_location}
- Accessibility Needs: {accessibility_needs}
- Query: {user_query}

Facilities Available:
- Bathrooms: 4 (2 accessible)
- Food Courts: 3
- Medical: Emergency + First Aid

Instructions:
1. Understand the user's need (direction, facility, info)
2. Check accessibility requirements
3. Suggest shortest and safest route
4. Include wait times and crowd info
5. Be friendly and concise
6. Respond in 2-3 sentences max

Respond naturally and helpfully."""
    
    return context

def call_groq(prompt: str) -> str:
    """Call Groq API (cloud LLM)"""
    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No response").strip()
        else:
            return f"Error: API returned {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to AI service. Check internet connection."
    except Exception as e:
        return f"Error: {str(e)}"

def generate_response(user_query: str, user_location: str, accessibility_needs: str) -> dict:
    """Generate AI response for user query"""
    
    context = build_context(user_query, user_location, accessibility_needs)
    prompt = f"{context}\n\nNow respond to the user's query."
    
    ai_response = call_groq(prompt)
    
    return {
        "response": ai_response,
        "user_location": user_location,
        "accessibility": accessibility_needs,
        "crowd_status": get_crowd_status(),
    }