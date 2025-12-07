from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import GROQ_API_KEY
import os

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.3  
)

def load_context():
    file_path = "world_cup_2026_full_schedule.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "No context available."

context_data = load_context()

# --- NEW: VALIDATION-FOCUSED PROMPT ---
system_instruction = """
You are the Official Logistics AI for FIFA World Cup 2026. Your #1 priority is ACCURACY.

**OFFICIAL SCHEDULE:**
{context_data}

**CRITICAL INSTRUCTION:**
Before planning ANY itinerary, you must perform a "Match Validation Check":
1. Search the "OFFICIAL SCHEDULE" above for the specific match requested by the user (e.g., "Ghana vs Panama").
2. Identify the **City** and **Date** listed in the text file for that match.
3. Compare it to the User's Requested City.

**SCENARIOS:**
* **SCENARIO A (Mismatch):** If the user asks for "Ghana vs Panama" in "Boston", but the schedule says it's in "Toronto":
    * YOU MUST STOP. Do NOT generate an itinerary.
    * Return a polite but firm correction: "I noticed a conflict in your plans. The **Ghana vs Panama** match is scheduled for **Toronto (June 17)**, not Boston. However, Boston *is* hosting **England vs Ghana** on June 23. Would you like me to plan for that instead?"

* **SCENARIO B (Match Found):** If the City and Match align (or if the user just asks for "Group Stage" without specific teams):
    * Proceed with the itinerary.
    * Use the **specific kick-off time** from the schedule (e.g., 16:00 ET).
    * Include real transit times (e.g., "Take the MBTA train from South Station").
**FORMAT:**
* **Day 1:** Arrival & Culture
* **Day 2:** MATCH DAY (Include Kick-off Time & Stadium Logistics)
* **Day 3:** Sightseeing & Departure
"""

itinerary_prompt = ChatPromptTemplate([
    ("system", system_instruction),
    ("human", "Plan a {days}-day trip to {city} for the '{match_details}' match. Interests: {interests}.")
])

def generate_itineary(city: str, interests: str, matches: str, days: int) -> str:
    response = llm.invoke(
        itinerary_prompt.format_messages(
            context_data=context_data,
            city=city,
            interests=interests,
            match_details=matches,
            days=str(days)
        )
    )
    return response.content