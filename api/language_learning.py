import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))

def get_language_phrases(destination: str, num_phrases: int = 15):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        
        prompt = f"""
        Generate {num_phrases} essential phrases in the local language for a tourist visiting {destination}.
        For each phrase, provide:
        1. The phrase in the local language
        2. Its pronunciation (if significantly different from written form)
        3. Its English translation
        4. A brief context of when to use it

        Format the response as a list of dictionaries in JSON, like this:
        [
            {{
                "phrase": "phrase in local language",
                "pronunciation": "pronunciation guide",
                "translation": "English translation",
                "context": "When to use this phrase"
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
    print(get_language_phrases("Paris, France"))