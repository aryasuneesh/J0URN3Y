import streamlit as st
from api.packing_list import generate_packing_list
import json

st.set_page_config(page_title="Packing List", page_icon="🧳", layout="wide")

st.title("Generate Packing List")

if 'all_data' in st.session_state:
    location = st.session_state['all_data']['location']
    interests = st.session_state['all_data']['interests']
    start_date = st.session_state['all_data']['start_date']
    end_date = st.session_state['all_data']['end_date']
    
    packing_list = json.loads(generate_packing_list(location, interests, start_date, end_date))
    
    for category, items in packing_list.items():
        with st.expander(category.capitalize()):
            for item in items:
                st.write(f"- {item}")
else:
    st.warning("Please generate an itinerary on the home page first.")