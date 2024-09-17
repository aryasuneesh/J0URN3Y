import os
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def parse_tips(text):
    tips = []
    pattern = r'\{\s*"tip"\s*:\s*"(.+?)"\s*,\s*"explanation"\s*:\s*"(.+?)"\s*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        tip = match[0].strip()
        explanation = match[1].strip()
        tips.append({"tip": tip, "explanation": explanation})
    
    return tips

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
        
        print("Debug - Raw response:", response.text)  # Debug print
        
        tips = parse_tips(response.text)
        
        if tips:
            return tips
        else:
            return {"error": "Failed to parse the response from the AI model."}
    
    except Exception as e:
        print(f"Debug - Exception occurred: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the function
    result = get_cultural_tips("Tokyo, Japan")
    print(json.dumps(result, indent=2))