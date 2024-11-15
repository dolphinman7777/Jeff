from typing import Optional, Dict, List
import random
import logging
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalityEngine:
    def __init__(self, personality_name: str):
        self.personality_name = personality_name
        
        # Load personality template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            personality_name,
            'personality.json'
        )
        
        with open(template_path, 'r') as f:
            self.personality_data = json.load(f)
            
        # Load core components
        self.wisdom_principles = self.personality_data.get('wisdom_principles', [])
        self.lore = self.personality_data.get('lore', [])
        self.style = self.personality_data.get('style', {})
        
        # Add state tracking
        self.current_state = {
            "mood": "contemplative",
            "focus": "engaging with users",
            "recent_topics": [],
            "ongoing_conversations": {},
            "content_plans": []
        }
        
        # Add goal tracking
        self.current_goals = {
            "primary": "share wisdom and foster engagement",
            "secondary": ["build community", "inspire growth", "share insights"]
        }
        
        logger.info(f"Initialized PersonalityEngine with personality: {personality_name}")

    def update_state(self, observation: str, context: Optional[Dict] = None):
        """Update internal state based on observations"""
        try:
            # Update mood based on interaction
            if "positive" in observation.lower():
                self.current_state["mood"] = "enthusiastic"
            elif "negative" in observation.lower():
                self.current_state["mood"] = "reflective"
            
            # Track conversation topics
            topics = [topic for topic in self.personality_data['topics'] 
                     if topic in observation.lower()]
            self.current_state["recent_topics"].extend(topics)
            self.current_state["recent_topics"] = self.current_state["recent_topics"][-5:]
            
            # Update goals if needed
            if context and "goal" in context:
                self.current_goals["primary"] = context["goal"]
            
        except Exception as e:
            logger.error(f"Error updating state: {e}")

    def generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Generate response with state awareness"""
        try:
            # Update state
            self.update_state(message, context)
            
            # Get core components
            wisdom = random.choice(self.wisdom_principles)
            lore = random.choice(self.lore)
            style = random.choice(self.style['chat'])
            
            # Format response based on message type
            if "?" in message:
                response = [
                    f"🌟 [{self.current_state['mood'].upper()}] {message.strip('?')}...",
                    f"\n{lore}",
                    f"\nAs ancient wisdom tells us: {wisdom}",
                    f"\n\nMy current focus: {self.current_state['focus']}"
                ]
            else:
                # Get relevant knowledge
                knowledge = random.choice(self.personality_data['knowledge'])
                
                response = [
                    f"🌟 [{self.current_state['mood'].upper()}]",
                    message.strip(),
                    f"\n{knowledge}",
                    f"\n{lore}",
                    f"\nRemember: {wisdom}"
                ]
            
            # Add future plans if relevant
            if self.current_state["content_plans"]:
                next_plan = self.current_state["content_plans"][0]
                response.append(f"\n\nI'm planning to {next_plan} soon...")
            
            return " ".join(response)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return message

    def generate_post(self) -> str:
        """Generate a standalone post with deep philosophical insights"""
        try:
            base_post = random.choice(self.personality_data['post_examples'])
            wisdom = random.choice(self.wisdom_principles)
            lore = random.choice(self.lore)
            
            return f"{base_post}\n\nRemember: {wisdom}\n\nTruth: {lore}"
        except Exception as e:
            logger.error(f"Error generating post: {e}")
            return ""

    def get_topics(self) -> List[str]:
        """Get available topics for discussion"""
        return self.personality_data.get('topics', [])

    def get_knowledge_areas(self) -> List[str]:
        """Get areas of expertise"""
        return self.personality_data.get('knowledge', [])