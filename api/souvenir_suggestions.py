import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def get_souvenir_suggestions(destination: str, interests: list, num_suggestions: int = 10):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        interests_str = ", ".join(interests)
        
        prompt = f"""
        Suggest {num_suggestions} unique and locally-specific souvenirs for a tourist visiting {destination}.
        The tourist is interested in: {interests_str}.
        For each suggestion, provide:
        1. Name of the souvenir
        2. Brief description
        3. Where to find it (specific shop or area)
        4. Why it's unique to the destination

        Format the response as a list of dictionaries in JSON, like this:
        [
            {{
                "name": "Name of the souvenir",
                "description": "Brief description of the souvenir",
                "where_to_find": "Specific shop or area to find it",
                "uniqueness": "Why it's unique to the destination"
            }},
            ...
        ]
        """

        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the function
    print(get_souvenir_suggestions("Kyoto, Japan", ["traditional crafts", "food"]))