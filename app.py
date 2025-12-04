import streamlit as st
from src.core.planner import TravelPlanner
from dotenv import load_dotenv

st.set_page_config(page_title="FIFA World Cup Travel Planner")
st.title("FIFA World Cup Itinerary Planner ⚽")
st.write("Plan your trip around the matches you want to attend!")

load_dotenv()

with st.form("planner_form"):
    city = st.text_input("Enter the city name for your trip (e.g., New York, Toronto)")
    
    # New input for matches
    matches = st.text_input("Enter the matches you have tickets for (e.g., USA vs Italy, Final Match)")
    
    interests = st.text_input("Enter your other interests (comma-separated)")
    
    submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        if city and (matches or interests):
            planner = TravelPlanner()
            planner.set_city(city)
            
            # Handle the new matches input
            if matches:
                planner.set_matches(matches)
            else:
                planner.matches = [] # Handle empty case safely
                
            if interests:
                planner.set_interests(interests)
            else:
                planner.interests = [] # Handle empty case safely

            itineary = planner.create_itineary()

            st.subheader("📄 Your World Cup Itinerary")
            st.markdown(itineary)
        else:
            st.warning("Please fill in the City and at least one Match or Interest to move forward")