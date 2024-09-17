import streamlit as st
import json
from api.language_learning import get_language_phrases

st.set_page_config(page_title="Language Learning", page_icon="🗣️", layout="wide")

st.title("Language Learning Resources")

if 'all_data' in st.session_state:
    location = st.session_state['all_data']['location']
    phrases = json.loads(get_language_phrases(location))
    
    for phrase in phrases:
        with st.expander(f"{phrase['phrase']}"):
            st.write(f"**Pronunciation:** {phrase['pronunciation']}")
            st.write(f"**Translation:** {phrase['translation']}")
            st.write(f"**Context:** {phrase['context']}")
else:
    st.warning("Please generate an itinerary on the home page first.")