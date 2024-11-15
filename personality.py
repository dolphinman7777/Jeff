from typing import Dict, List, Optional
import random
from enum import Enum
import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Trait(Enum):
    FRIENDLINESS = "friendliness"
    FORMALITY = "formality"
    CREATIVITY = "creativity"
    ASSERTIVENESS = "assertiveness"
    EMPATHY = "empathy"

@dataclass
class PersonalityConfig:
    traits: Dict[Trait, float]
    tone_modifiers: Dict[str, List[str]]
    response_templates: Dict[str, List[str]]

class PersonalityEngine:
    def __init__(self, config: Optional[PersonalityConfig] = None):
        self.traits = config.traits if config else {
            Trait.FRIENDLINESS: 0.7,
            Trait.FORMALITY: 0.5,
            Trait.CREATIVITY: 0.6,
            Trait.ASSERTIVENESS: 0.4,
            Trait.EMPATHY: 0.8
        }
        
        self.tone_modifiers = {
            "friendly": ["😊", "Great question!", "Happy to help!"],
            "formal": ["I understand", "Certainly", "Indeed"],
            "creative": ["Let's explore", "Here's an interesting approach", "Imagine"],
            "assertive": ["Definitely", "Without doubt", "Absolutely"],
            "empathetic": ["I see where you're coming from", "I understand that", "That makes sense"]
        }

        self.response_templates = {
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! Ready to help!",
                "Greetings! What can I do for you?"
            ],
            "confirmation": [
                "I'll take care of that",
                "Consider it done",
                "I'm on it"
            ],
            "error": [
                "I encountered an issue",
                "There seems to be a problem",
                "Something went wrong"
            ]
        }

    def adjust_trait(self, trait: Trait, value: float) -> None:
        """Adjust a personality trait within bounds."""
        logger.info(f"Adjusting trait {trait.value} from {self.traits[trait]} to {value}")
        self.traits[trait] = max(0.0, min(1.0, value))

    def get_response_tone(self, context: str) -> str:
        """Generate appropriate tone based on personality traits and context."""
        dominant_trait = max(self.traits.items(), key=lambda x: x[1])
        
        if dominant_trait[0] == Trait.FRIENDLINESS:
            return random.choice(self.tone_modifiers["friendly"])
        elif dominant_trait[0] == Trait.FORMALITY:
            return random.choice(self.tone_modifiers["formal"])
        # ... similar for other traits
        
        return random.choice(self.tone_modifiers["formal"])  # default

    def generate_response(self, message_type: str, context: Dict[str, any]) -> str:
        """Generate a personality-influenced response."""
        try:
            base_template = random.choice(self.response_templates[message_type])
            tone_modifier = self.get_response_tone(str(context))
            
            # Apply personality traits influence
            if self.traits[Trait.FRIENDLINESS] > 0.7:
                base_template = f"{tone_modifier} {base_template}"
            
            if self.traits[Trait.FORMALITY] > 0.7:
                base_template = base_template.replace("!", ".")
                
            if self.traits[Trait.CREATIVITY] > 0.7:
                base_template = f"{base_template} ✨"
                
            logger.info(f"Generated response with type {message_type}")
            return base_template
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I'm having trouble formulating a response."

    def adapt_to_user(self, user_message: str) -> None:
        """Adapt personality traits based on user interaction."""
        # Sentiment analysis could be added here
        message_length = len(user_message.split())
        
        if message_length > 20:
            self.adjust_trait(Trait.FORMALITY, self.traits[Trait.FORMALITY] + 0.1)
        else:
            self.adjust_trait(Trait.FORMALITY, self.traits[Trait.FORMALITY] - 0.1) 