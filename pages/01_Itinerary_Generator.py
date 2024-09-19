import streamlit as st
from api.map_generator import display_map

st.set_page_config(page_title="Itinerary Generator", page_icon="🗺️", layout="wide")

st.title("Your Personalized Itinerary!")

if 'all_data' in st.session_state:
    for day in st.session_state['all_data']["itinerary"]:
        with st.expander(f"Date: {day['date']} - {day['activity']}"):
            st.write(f"**Place**: {day['place']}")
            st.write(f"**Activity**: {day['activity']}")
            st.write(f"**Description**: {day['description']}")
            
            st.subheader("Location Map")
            display_map(day['place'])
else:
    st.warning("Please generate an itinerary on the home page first.")