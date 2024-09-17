import streamlit as st
from api.cultural_sensitivity import get_cultural_tips

st.set_page_config(page_title="Cultural Tips", page_icon="🌍", layout="wide")

st.title("Cultural Sensitivity Tips")

if 'all_data' in st.session_state:
    location = st.session_state['all_data']['location']
    try:
        tips = get_cultural_tips(location)
        
        if isinstance(tips, list) and tips:
            for tip in tips:
                with st.expander(f"{tip['tip']}"):
                    st.write(f"**Explanation:** {tip['explanation']}")
        elif isinstance(tips, dict) and 'error' in tips:
            st.error(f"Error: {tips['error']}")
            st.error("Unable to generate cultural tips at this time. Please try again later.")
        elif isinstance(tips, list) and not tips:
            st.warning(f"No cultural tips were found for {location}. This might be due to limited information or an error in processing.")
        else:
            st.warning("Unexpected data format received. Please contact support if this issue persists.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please try again later or contact support if the issue persists.")
else:
    st.warning("Please generate an itinerary on the home page first.")