import streamlit as st
from api.itinerary_generator import generate_itinerary
from api.parse_itinerary import parse_itinerary
from api.map_generator import display_map

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
                            # Display map
                            st.subheader("Location Map")
                            display_map(day['place'] + "," + location)
        else:
            st.error("Please fill out all fields.")

# Additional feature buttons (below the itinerary display in the right column)
with right_col:
    st.header("Enhance Your Travel Experience")

    # Language learning button (placeholder)
    if st.button("Language Learning Resources"):
        st.info("Language learning resources feature coming soon!")

    # Souvenir suggestions button (placeholder)
    if st.button("Personalized Souvenir Suggestions"):
        st.info("Personalized souvenir suggestions feature coming soon!")