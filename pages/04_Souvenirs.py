import streamlit as st
from api.souvenir_suggestions import get_souvenir_suggestions
import json

st.set_page_config(page_title="Souvenir Suggestions", page_icon="🛍️", layout="wide")

st.title("Personalized Souvenir Suggestions")

if 'all_data' in st.session_state:
    location = st.session_state['all_data']['location']
    interests = st.session_state['all_data']['interests']
    souvenirs = json.loads(get_souvenir_suggestions(location, interests))
    
    for souvenir in souvenirs:
        with st.expander(f"{souvenir['name']}"):
            st.write(f"**Description:** {souvenir['description']}")
            st.write(f"**Where to find:** {souvenir['where_to_find']}")
            st.write(f"**Uniqueness:** {souvenir['uniqueness']}")
else:
    st.warning("Please generate an itinerary on the home page first.")