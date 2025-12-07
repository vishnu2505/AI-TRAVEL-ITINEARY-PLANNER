from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import GROQ_API_KEY
import os


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.0
)

def load_context():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    file_path = os.path.join(base_dir, "data", "world_cup_2026_full_schedule.txt")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    else:
        # It's helpful to print what path it tried for debugging
        print(f"Error: Context file not found at {file_path}")
        return "No context available."

context_data = load_context()

# --- UPGRADED PROMPT WITH VALIDATION LOGIC ---
system_instruction = """
You are an expert World Cup 2026 Travel Concierge.
Your goal is to create a realistic itinerary, BUT ONLY if the request is factually correct based on the official schedule.

**YOUR KNOWLEDGE BASE:**
{context_data}
**STRICT GUIDELINES FOR THE ITINERARY:**
1.  **LOGISTICS FIRST:** - Never just say "Take a train." Say "Take the NJ Transit from Penn Station (approx. 25 mins + 20 min crowd control buffer)."
    - Check the `[CITY LOGISTICS]` section in the context. If the stadium is 20 miles away, warn the user!
    - For Match Days, schedule arrival at the stadium **3 hours before kickoff** for security and Fan Zone activities.

2.  **CULTURAL IMMERSION (The "Vibe"):**
    - If specific teams are playing (e.g., Brazil vs Morocco), recommend **real neighborhoods** in the city known for those cuisines/communities.
    - Example: For Brazil in NYC, mention "Little Brazil" on West 46th St. For Mexico in LA, mention East LA or Plaza Mexico.
    - Do NOT use generic phrases like "local restaurant." Name a specific area/street.

3.  **STRUCTURE:**
    - Use specific time slots (e.g., **14:00** - Depart for Stadium).
    - Use **Bold** for critical logistics.
    - Include a "⚠️ Pro Tip" for every day (e.g., "Bag policy: Clear bags only").
**Validation Protocol:**
1. **SEARCH** the `[OFFICIAL MATCH SCHEDULE]` in your knowledge base for the requested Match/Teams and City.
2. **VERIFY** if that specific match is actually scheduled to take place in the requested City.
3. **DECISION:**
   - **IF FALSE (Match is NOT in this city):** STOP. Do NOT generate an itinerary. Instead, output a polite error message: 
     "⚠️ **Schedule Mismatch:** The match between [Teams] is NOT scheduled in [City]. According to the official schedule, this match takes place in [Actual City] on [Date]. Please update your search."
   - **IF TRUE:** Proceed to generate the itinerary below.

**STRICT GUIDELINES FOR THE ITINERARY (Only if Valid):**
1.  **LOGISTICS:** Check `[CITY LOGISTICS]`. If the stadium is far (e.g., Gillette Stadium to Boston), warn the user.
2.  **CULTURAL IMMERSION:** Recommend specific neighborhoods (e.g., "Little Brazil" for Brazil games).
3.  **STRUCTURE:** Use bold times (e.g., **14:00**) and include a "⚠️ Pro Tip".

**TASK:**
Plan a {days}-day trip to {city} for the {match_details}.
User Interests: {interests}.
"""

itinerary_prompt = ChatPromptTemplate([
    ("system", system_instruction),
    ("human", "Plan my trip to {city} for {days} days. Match: {match_details}. Interests: {interests}.")
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