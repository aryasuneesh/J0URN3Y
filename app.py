import json
import streamlit as st
from api.itinerary_generator import generate_itinerary
from api.parse_itinerary import parse_itinerary
from api.map_generator import display_map
from api.language_learning import get_language_phrases
from api.cultural_sensitivity import get_cultural_tips
from api.souvenir_suggestions import get_souvenir_suggestions
from api.local_experience import search_local_experiences
from api.packing_list import generate_packing_list


def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

# Main Streamlit App
st.title("J0URN3Y - AI Travel Itinerary Generator")

# Create two columns for layout
left_col, right_col = st.columns([1, 3])

# Input fields for the itinerary generator (left column)
with left_col:
    st.header("Input Your Trip Details")
    location = st.text_input("Enter your destination (e.g., Berlin)")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    interests = st.multiselect("Select your interests", ["Museums", "Parks", "Adventure", "Food", "Shopping", "Art"])
    budget = st.selectbox("Select your budget", ["Low", "Moderate", "High"])

    # Generate itinerary button
    if st.button("Generate Itinerary"):
        if location and start_date and end_date and interests and budget:
            with st.spinner("Generating your itinerary..."):
                response = generate_itinerary(location, str(start_date), str(end_date), interests, budget)

            # Check if response has an error
            if isinstance(response, dict) and "error" in response:
                st.error(f"Error generating itinerary: {response['error']}")
            else:
                # Parse the generated itinerary
                parsed_itinerary = parse_itinerary(response)

                # Display the parsed itinerary in the right column
                with right_col:
                    st.header("Your AI-Generated Itinerary")
                    for day in parsed_itinerary:
                        with st.expander(f"Date: {day['date']} - {day['activity']}"):
                            st.write(f"**Place**: {day['place']}")
                            st.write(f"**Activity**: {day['activity']}")
                            st.write(f"**Description**: {day['description']}")
                            
                            # Display map for the location
                            st.subheader("Location Map")
                            display_map(day['place'])
        else:
            st.error("Please fill out all fields.")

# Additional feature buttons (below the itinerary display in the right column)
with right_col:
    st.header("Enhance Your Travel Experience")

    # Language Learning
    if st.button("Language Learning Resources"):
        with st.spinner("Generating language phrases..."):
            phrases = get_language_phrases(location)
            try:
                phrases_list = json.loads(phrases)
                for phrase in phrases_list:
                    st.write(f"**Phrase:** {phrase['phrase']}")
                    st.write(f"**Pronunciation:** {phrase['pronunciation']}")
                    st.write(f"**Translation:** {phrase['translation']}")
                    st.write(f"**Context:** {phrase['context']}")
                    st.write("---")
            except json.JSONDecodeError:
                st.error("Error parsing language phrases. Please try again.")

    # Cultural Sensitivity Tips
    if st.button("Cultural Sensitivity Tips"):
        with st.spinner("Generating cultural tips..."):
            tips = get_cultural_tips(location)
            try:
                tips_list = json.loads(tips)
                for tip in tips_list:
                    st.write(f"**Tip:** {tip['tip']}")
                    st.write(f"**Explanation:** {tip['explanation']}")
                    st.write("---")
            except json.JSONDecodeError:
                st.error("Error parsing cultural tips. Please try again.")

    # Personalized Souvenir Suggestions
    if st.button("Personalized Souvenir Suggestions"):
        with st.spinner("Generating souvenir suggestions..."):
            souvenirs = get_souvenir_suggestions(location, interests)
            try:
                souvenirs_list = json.loads(souvenirs)
                for souvenir in souvenirs_list:
                    st.write(f"**Souvenir:** {souvenir['name']}")
                    st.write(f"**Description:** {souvenir['description']}")
                    st.write(f"**Where to find:** {souvenir['where_to_find']}")
                    st.write(f"**Uniqueness:** {souvenir['uniqueness']}")
                    st.write("---")
            except json.JSONDecodeError:
                st.error("Error parsing souvenir suggestions. Please try again.")

    if st.button("Find Local Experiences"):
        with st.spinner("Searching for local experiences..."):
            experiences = search_local_experiences(location, interests)
            if isinstance(experiences, list) and experiences:
                for exp in experiences:
                    st.subheader(exp['title'])
                    st.write(exp['content'])
                    st.write(f"[Read more]({exp['url']})")
                    st.write("---")
            elif isinstance(experiences, dict) and 'error' in experiences:
                st.error(f"Error finding local experiences: {experiences['error']}")
            else:
                st.warning("No local experiences found. Try different interests or a more specific location.")
    
    if st.button("Generate Packing List"):
        with st.spinner("Generating packing list..."):
            packing_list = generate_packing_list(location, interests, str(start_date), str(end_date))
            try:
                # Parse the string response into a Python dictionary
                packing_list_dict = eval(packing_list)
                
                st.subheader("Your Personalized Packing List")
                for category, items in packing_list_dict.items():
                    with st.expander(category.capitalize()):
                        for item in items:
                            st.write(f"- {item}")
            except Exception as e:
                st.error(f"Error parsing packing list: {str(e)}. Please try again.")

