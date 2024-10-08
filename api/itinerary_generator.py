import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
from typing import List, Dict, Any

# Configuration for Google AI Studio API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def generate_itinerary(location: str, start_date: str, end_date: str, interests: List[str], budget: str) -> Dict[str, Any]:
    try:
        model = genai.GenerativeModel(
            "gemini-1.5-flash-latest",
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
        Generate a travel itinerary in JSON format for a trip to {location} from {start_date} to {end_date}.
        The user is interested in {', '.join(interests)} and has a budget of {budget}.
        
        Use this JSON schema:
        Itinerary = {{
            'place': str, 
            'date': str, 
            'activity': str, 
            'description': str
        }}
        
        Return: list[Itinerary]
        """

        response = model.generate_content(prompt)
        response_dict = response.to_dict()
        itinerary_json = response_dict["candidates"][0]["content"]["parts"][0]["text"]
        
        # Parse the JSON string into a Python object
        itinerary_list = json.loads(itinerary_json)
        
        # Create the complete itinerary object
        complete_itinerary = {
            'location': location,
            'start_date': start_date,
            'end_date': end_date,
            'interests': interests,
            'budget': budget,
            'itinerary': itinerary_list
        }
        
        return complete_itinerary
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage for testing
    example_itinerary = generate_itinerary(
        location="Paris", 
        start_date="15-09-2024", 
        end_date="20-09-2024", 
        interests=["museums", "parks", "adventure"], 
        budget="moderate"
    )
    print(json.dumps(example_itinerary, indent=2))