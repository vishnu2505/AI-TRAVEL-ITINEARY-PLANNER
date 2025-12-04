from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.config.config import GROQ_API_KEY

llm = ChatGroq(
    groq_api_key = GROQ_API_KEY,
    model_name = "llama-3.3-70b-versatile",
    temperature=0.3
)

# Updated prompt to include matches
itnineary_prompt = ChatPromptTemplate([
    ("system", "You are a helpful travel assistant. Create a detailed itinerary for {city} during the FIFA World Cup. "
               "The user plans to attend the following matches: {matches}. "
               "Also consider the user's other interests: {interests}. "
               "Ensure the itinerary allocates appropriate time for match attendance (including travel to stadium) "
               "and balances it with sightseeing. Provide a brief, bulleted itinerary."),
    ("human", "Create an itinerary for my trip")
])

def generate_itineary(city: str, interests: list[str], matches: list[str]) -> str:
    response = llm.invoke(
        itnineary_prompt.format_messages(
            city=city,
            interests=', '.join(interests),
            matches=', '.join(matches)
        )
    )
    return response.content