import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from streamlit_folium import folium_static

def generate_map(place: str):
    geolocator = Nominatim(user_agent="j0urn3y_app")
    
    try:
        # Attempt to geocode the place
        location = geolocator.geocode(place)
        
        if location:
            # Create a map centered on the location
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=13)
            
            # Add a marker for the location
            folium.Marker(
                [location.latitude, location.longitude],
                popup=place,
                tooltip=place
            ).add_to(m)
            
            return m
        else:
            st.warning(f"Could not find location for: {place}")
            return None
    
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        st.error(f"Error generating map: {str(e)}")
        return None

def display_map(place: str):
    map_obj = generate_map(place)
    if map_obj:
        folium_static(map_obj)
    else:
        st.warning("Unable to display map for this location.")

if __name__ == "__main__":
    place = "Eiffel Tower, Paris"
    display_map(place)