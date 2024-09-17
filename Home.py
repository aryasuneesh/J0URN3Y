import streamlit as st
import json
from api.itinerary_generator import generate_itinerary
from api.parse_itinerary import parse_itinerary
from api.map_generator import display_map
from sqlite_cache import get_db_connection, cache_api_call, is_valid_itinerary, print_cache_contents

st.set_page_config(page_title="J0URN3Y", page_icon=":bridge_at_night:", layout="wide")

activities = [
    "Adventure", "Food", "Walking", "Museums", "Sightseeing", "Water Activities",
    "Hiking", "Shopping", "Relaxing", "Exploring", "Photography", "Beach"
]

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: black;
    }
    .stButton > button {
        background-color: #D7BCC8;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# App header
col1, col2 = st.columns([2, 5])
with col1:
    st.image("assets/logo.png", width=350)
with col2:
    st.markdown("# :rainbow[AI-powered Travel Itinerary Generator]")

# Input fields
location = st.text_input("Enter your destination (e.g., Berlin, Paris)")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
interests = st.multiselect("Select your interests", activities)
budget = st.selectbox("Select your budget", ["Low", "Moderate", "High"])

if st.button("Generate Itinerary"):
    if location and start_date and end_date and interests and budget:
        with st.spinner("Generating your itinerary..."):
            complete_itinerary = cache_api_call(generate_itinerary, location, str(start_date), str(end_date), interests, budget)
            
            # Debug: Print raw generated data
            st.write("Debug: Raw Generated Data")
            st.json(complete_itinerary)
            
            if is_valid_itinerary(complete_itinerary):
                st.session_state['all_data'] = complete_itinerary
                st.success("Itinerary generated! Navigate to other pages to see more details.")
            else:
                st.error("Error: Generated data is not a valid itinerary")
            
            # Debug: Print cache contents
            # st.write("Debug: Cache Contents")
            # print_cache_contents()
            # st.write("Check your console for cache contents")
    else:
        st.error("Please fill out all fields.")

# HISTORY

st.header("Itinerary History")
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT key, value FROM cache")
history = cursor.fetchall()
conn.close()

# Debug: Print raw database contents
# st.write("Debug: Raw Database Contents")
# st.write(history)

if not history:
    st.info("No itineraries found. Generate your first itinerary to get started!")
else:
    for key, value in history:
        try:
            data = json.loads(value)
            if is_valid_itinerary(data):
                location = data['location']
                start_date = data['start_date']
                with st.expander(f"Trip to {location} on {start_date}"):
                    if st.button(f"Load this itinerary", key=f"load_{key}"):
                        st.session_state['all_data'] = data
                        st.experimental_rerun()
                    
                    # Display itinerary details
                    st.write(f"**Destination:** {location}")
                    st.write(f"**Date:** {start_date} to {data['end_date']}")
                    st.write(f"**Interests:** {', '.join(data['interests'])}")
                    st.write(f"**Budget:** {data['budget']}")
                    
                    for day in data['itinerary']:
                        st.subheader(f"Date: {day['date']} - {day['activity']}")
                        st.write(f"**Place:** {day['place']}")
                        st.write(f"**Activity:** {day['activity']}")
                        st.write(f"**Description:** {day['description']}")
                        display_map(day['place'])
            else:
                st.warning(f"Invalid data found in cache for key: {key}. Please regenerate this itinerary.")
        except json.JSONDecodeError:
            st.warning(f"Corrupted data found in cache for key: {key}. Please regenerate this itinerary.")
        except Exception as e:
            st.error(f"An error occurred while loading itinerary with key: {key}. Error: {str(e)}")