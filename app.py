import streamlit as st
from api.itinerary_generator import generate_itinerary
from api.parse_itinerary import parse_itinerary  # Add the parsing function here

# Streamlit UI
st.title("J0URN3Y - AI-Powered Travel Itinerary Generator")

# User input form
location = st.text_input("Enter your destination")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
interests = st.multiselect("Select your interests", 
                           ["sightseeing", "museums", "parks", "adventure", "water activities", 
                            "foodie", "walking", "beaches", "shopping"])
budget = st.selectbox("Select your budget", ["low", "moderate", "high"])

# Button to generate itinerary
if st.button("Generate Itinerary"):
    if location and start_date and end_date and interests and budget:
        # Call the itinerary generator
        response = generate_itinerary(
            location=location, 
            start_date=start_date.strftime('%d-%m-%Y'), 
            end_date=end_date.strftime('%d-%m-%Y'), 
            interests=interests, 
            budget=budget
        )
        
        # Parse and display the itinerary
        formatted_itinerary = parse_itinerary(response)
        st.markdown(formatted_itinerary)

    else:
        st.error("Please fill all the fields to generate the itinerary.")
