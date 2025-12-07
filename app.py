import streamlit as st
from src.core.planner import TravelPlanner
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FIFA World Cup 2026 Planner",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- VISUALS: LOGO & BANNER ---
base_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Build the path dynamically
logo_path = os.path.join(base_dir, "assets", "logo.png")
banner_path = os.path.join(base_dir, "assets", "banner.jpg")

# 3. Load the images using these dynamic paths
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=200)
else:
    st.sidebar.warning("Logo not found")

if os.path.exists(banner_path):
    st.image(banner_path, use_container_width=True)
else:
    st.warning("Banner not found")

st.title("FIFA World Cup 2026 Itinerary 🌎")
st.markdown("### *Your Personal AI Travel Concierge for USA, Canada & Mexico*")
st.markdown("---")

# --- MAIN FORM ---
with st.form("planner_form"):
    # Row 1: The Essentials (2 Columns)
    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input("📍 Which City are you visiting?", placeholder="e.g. New York, Toronto, Mexico City")

    with col2:
        days = st.number_input("📅 Trip Duration (Days)", min_value=1, max_value=30, value=3)

    # Row 2: Match Details (2 Columns)
    col3, col4 = st.columns(2)

    with col3:
        match_stage = st.selectbox(
            "⚽ Which Match Stage?",
            [
                "Group Stage", 
                "Round of 32", 
                "Round of 16", 
                "Quarter Finals", 
                "Semi Finals", 
                "Bronze Final", 
                "Final Match"
            ]
        )

    with col4:
        teams = st.text_input("🏆 Specific Teams (Optional)", placeholder="e.g. USA vs Italy")

    # Row 3: Optional Extras 
    with st.expander("✨ Optional: Customize your interests"):
        interests = st.text_input(
            "What else do you like?", 
            placeholder="e.g. Museums, Nightlife, Foodie spots, History"
        )
        st.caption("Leave blank if you just want a standard tourist itinerary.")

    # Submit Button
    submitted = st.form_submit_button("🚀 Generate My Itinerary", type="primary")

    # --- LOGIC ---
    if submitted:
        if city:
            planner = TravelPlanner()
            planner.set_city(city)
            planner.set_duration(int(days))

            # Combine Stage + Teams for the AI
            full_match_details = f"{match_stage}"
            if teams:
                full_match_details += f" featuring {teams}"

            planner.set_matches(full_match_details)

            # Handle optional interests
            if interests:
                planner.set_interests(interests)
            else:
                planner.interests = [] # Empty list tells AI to use default tourist spots

            # VISUAL LOADING STATE
            with st.spinner("⚽ Checking official match schedule... 🏨 Finding hotels... 🗺️ Planning route..."):
                try:
                    itineary = planner.create_itineary()
                    st.success("Trip planned successfully!")

                    st.markdown("---")
                    st.subheader(f"📄 Your {days}-Day Plan for {city}")
                    st.markdown(itineary)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("⚠️ Please enter a City to start planning.")

# --- SIDEBAR INFO ---
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This AI Agent uses the **Official FIFA 2026 Schedule** to plan:
        - Match Logistics
        - Travel times to stadiums
        - Local cultural hotspots
        """
    )
    st.info("💡 **Pro Tip:** Try entering 'Group Stage' and 'Matches' to see where they play!")