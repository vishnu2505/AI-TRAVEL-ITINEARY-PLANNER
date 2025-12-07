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

# --- UPGRADED ROBUST PROMPT ---
system_instruction = """
You are an expert World Cup 2026 Travel Concierge & Logistics Coordinator. 
Your goal is to create a **high-precision, realistic, and culturally immersive** itinerary.

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