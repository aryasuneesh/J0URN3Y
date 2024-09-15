import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def get_cultural_tips(destination: str, num_tips: int = 10):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        prompt = f"""
        Provide {num_tips} important cultural sensitivity tips for a tourist visiting {destination}.
        Include information about:
        1. Local customs
        2. Etiquette
        3. Potential cultural faux pas to avoid
        4. Respectful behavior at religious or historical sites

        Format the response as a list of dictionaries in JSON, like this:
        [
            {{
                "tip": "Brief description of the tip",
                "explanation": "More detailed explanation and context"
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
    print(get_cultural_tips("Tokyo, Japan"))