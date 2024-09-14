import json
from typing import Any, Dict, List

def parse_itinerary(itinerary_json: str) -> List[Dict[str, Any]]:
    try:
        # Load the JSON string into a Python list of dictionaries
        itinerary_data = json.loads(itinerary_json)
        
        # Initialize an empty list to store parsed details
        parsed_itinerary = []
        
        for item in itinerary_data:
            place = item.get("place", "Unknown place")
            date = item.get("date", "Unknown date")
            activity = item.get("activity", "No activity specified")
            description = item.get("description", "No description available")

            # Create a formatted entry for each itinerary item
            formatted_entry = {
                "place": place,
                "date": date,
                "activity": activity,
                "description": description
            }
            
            # Append the formatted entry to the parsed itinerary list
            parsed_itinerary.append(formatted_entry)
        
        return parsed_itinerary

    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage for testing
    raw_json = """
    [
        {
            "place": "Paris, France",
            "date": "15-09-2024",
            "activity": "Arrival and Check-in",
            "description": "Arrive at Charles de Gaulle Airport (CDG), take the RER B train to the city center, and check into your moderately priced hotel."
        },
        {
            "place": "Eiffel Tower",
            "date": "16-09-2024",
            "activity": "Morning Climb & Champ de Mars Picnic",
            "description": "Start your day with an invigorating climb to the second level of the Eiffel Tower."
        }
    ]
    """
    parsed = parse_itinerary(raw_json)
    print(parsed)
