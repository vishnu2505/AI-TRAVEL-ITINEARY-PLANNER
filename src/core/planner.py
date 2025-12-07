from langchain_core.messages import HumanMessage, AIMessage
from src.chains.itinerary_chain import generate_itineary
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException

logger = get_logger(__name__)

class TravelPlanner:
    def __init__(self):
        self.messages = []
        self.city = ""
        self.interests = []
        self.matches = []
        self.days = 1  # Default to 1 day
        self.itineary = ""

        logger.info("Initialized TravelPlanner instance")

    def set_city(self, city: str):
        try:
            self.city = city
            self.messages.append(HumanMessage(content=f"City: {city}"))
            logger.info("City set successfully")
        except Exception as e:
            logger.error(f"Error while setting city: {e}")
            raise CustomException("Failed to set city", e)

    def set_interests(self, interests_str: str):
        try:
            self.interests = [i.strip() for i in interests_str.split(",")]
            self.messages.append(HumanMessage(content=f"Interests: {interests_str}"))
            logger.info("Interests set successfully")
        except Exception as e:
            logger.error(f"Error while setting interests: {e}")
            raise CustomException("Failed to set interests", e)

    def set_matches(self, matches_str: str):
        try:
            self.matches = [m.strip() for m in matches_str.split(",")]
            self.messages.append(HumanMessage(content=f"Matches: {matches_str}"))
            logger.info("Matches set successfully")
        except Exception as e:
            logger.error(f"Error while setting matches: {e}")
            raise CustomException("Failed to set matches", e)

    # NEW: Method to set the duration
    def set_duration(self, days: int):
        try:
            self.days = days
            self.messages.append(HumanMessage(content=f"Trip Duration: {days} days"))
            logger.info(f"Duration set to {days} days")
        except Exception as e:
            logger.error(f"Error while setting duration: {e}")
            raise CustomException("Failed to set duration", e)

    def create_itineary(self):
        try:
            logger.info(f"Generating itinerary for {self.city} ({self.days} days), matches: {self.matches}")

            # Pass 'days' to the generate function
            itineary = generate_itineary(self.city, self.interests, self.matches, self.days)

            self.itineary = itineary
            self.messages.append(AIMessage(content=itineary))
            logger.info("Itinerary generated successfully")
            return itineary
        except Exception as e:
            logger.error(f"Error while creating itinerary: {e}")
            raise CustomException("Failed to create itinerary", e)