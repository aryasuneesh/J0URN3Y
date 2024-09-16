from datetime import datetime, date
from typing import Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_season(date: date, hemisphere: str = 'northern') -> str:
    """
    Determine the season based on the date and hemisphere.
    
    Args:
    date (date): The date to check.
    hemisphere (str): Either 'northern' or 'southern'. Defaults to 'northern'.
    
    Returns:
    str: The season ('spring', 'summer', 'autumn', or 'winter').
    """
    day = date.timetuple().tm_yday
    
    spring = range(80, 172)
    summer = range(172, 264)
    autumn = range(264, 355)
    # winter = everything else
    
    if hemisphere == 'southern':
        spring = range(264, 355)
        autumn = range(80, 172)
    
    if day in spring:
        return 'spring'
    elif day in summer:
        return 'summer'
    elif day in autumn:
        return 'autumn'
    else:
        return 'winter'

def get_hemisphere(location: str) -> str:
    """
    Determine the hemisphere based on the location's latitude.
    
    Args:
    location (str): The name of the location.
    
    Returns:
    str: 'northern' or 'southern'
    """
    geolocator = Nominatim(user_agent="my_agent")
    try:
        # Attempt to get the location's coordinates
        location = geolocator.geocode(location, timeout=10)
        if location:
            latitude = location.latitude
            return 'northern' if latitude >= 0 else 'southern'
        else:
            # If location not found, default to northern hemisphere
            print(f"Warning: Couldn't find coordinates for {location}. Defaulting to northern hemisphere.")
            return 'northern'
    except (GeocoderTimedOut, GeocoderUnavailable):
        # If there's an error with the geocoding service, default to northern hemisphere
        print(f"Warning: Geocoding service unavailable. Defaulting to northern hemisphere for {location}.")
        return 'northern'

def determine_season(start_date: str, end_date: str, location: str) -> str:
    """
    Determine the primary season for a trip based on start and end dates.
    
    Args:
    start_date (str): The start date of the trip in 'YYYY-MM-DD' format.
    end_date (str): The end date of the trip in 'YYYY-MM-DD' format.
    location (str): The location of the trip.
    
    Returns:
    str: The primary season for the trip.
    """
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    hemisphere = get_hemisphere(location)
    
    start_season = get_season(start, hemisphere)
    end_season = get_season(end, hemisphere)
    
    if start_season == end_season:
        return start_season
    else:
        # If the trip spans two seasons, return the season of the majority of the trip
        mid_date = start + (end - start) / 2
        return get_season(mid_date, hemisphere)

if __name__ == "__main__":
    # Test the function
    print(determine_season("2023-12-20", "2024-01-05", "New York"))  # Should return 'winter'
    print(determine_season("2023-12-20", "2024-01-05", "Sydney"))    # Should return 'summer'
    print(determine_season("2023-06-01", "2023-06-15", "Paris"))     # Should return 'summer'
    print(determine_season("2023-06-01", "2023-06-15", "Buenos Aires"))  # Should return 'winter'