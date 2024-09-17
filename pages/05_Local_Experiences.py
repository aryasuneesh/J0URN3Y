import streamlit as st
from api.local_experience import search_local_experiences

st.set_page_config(page_title="Local Experiences", page_icon="🌟", layout="wide")

st.title("Find Local Experiences")

if 'all_data' in st.session_state:
    location = st.session_state['all_data']['location']
    interests = st.session_state['all_data']['interests']
    experiences = search_local_experiences(location, interests)
    
    for exp in experiences:
        with st.expander(f"{exp['title']}"):
            st.write(exp['content'])
            st.write(f"[Read more]({exp['url']})")
else:
    st.warning("Please generate an itinerary on the home page first.")