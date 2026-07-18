# AI integration with Ollama
from typing import Dict
import requests
import json
from stadium_data import (
    get_closest_facility,
    get_crowd_status,
    get_accessible_routes,
    STADIUM_DATA
)

OLLAMA_URL = "http://localhost:11434/api/generate"

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

def call_ollama(prompt: str) -> str:
    """Call local Ollama model"""
    try:
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Error: No response from model").strip()
        else:
            return f"Error: Model returned status {response.status_code}"
    
    except requests.exceptions.ConnectionError:
        return "Error: Ollama not running. Please run 'ollama serve' in another terminal."
    except Exception as e:
        return f"Error: {str(e)}"

def generate_response(user_query: str, user_location: str, accessibility_needs: str) -> Dict:
    """Generate AI response for user query"""
    
    context = build_context(user_query, user_location, accessibility_needs)
    
    prompt = f"{context}\n\nNow respond to the user's query."
    
    ai_response = call_ollama(prompt)
    
    return {
        "response": ai_response,
        "user_location": user_location,
        "accessibility": accessibility_needs,
        "crowd_status": get_crowd_status(),
    }