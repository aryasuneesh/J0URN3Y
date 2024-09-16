import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime
from api.season_generator import determine_season

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def generate_packing_list(destination: str, activities: list, start_date: str, end_date: str):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        activities_str = ", ".join(activities)
        duration = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        season = determine_season(start_date, end_date, destination)
        
        prompt = f"""
        Generate a personalized packing list for a {duration}-day trip to {destination} during {season}.
        The traveler plans to do the following activities: {activities_str}.

        Provide the packing list in the following categories:
        1. Clothing
        2. Footwear
        3. Toiletries
        4. Electronics
        5. Miscellaneous

        Format the response as a dictionary, like this:
        {{
            "clothing": ["item1", "item2", ...],
            "footwear": ["item1", "item2", ...],
            "toiletries": ["item1", "item2", ...],
            "electronics": ["item1", "item2", ...],
            "miscellaneous": ["item1", "item2", ...]
        }}
        """

        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the function
    print(generate_packing_list("Bali, Indonesia", ["beach", "hiking", "snorkeling"], "2023-07-01", "2023-07-08"))