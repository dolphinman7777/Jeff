from typing import List, Dict, Tuple
from dataclasses import dataclass
import random
import re

@dataclass
class ConversationContext:
    history: List[Dict[str, str]] = None
    current_topic: str = None
    last_art: str = None
    
    def __post_init__(self):
        self.history = []
        
    def add_exchange(self, user_msg: str, response: str, art: str = None):
        self.history.append({
            "user": user_msg, 
            "response": response,
            "art": art
        })
        if art:
            self.last_art = art
        
    def get_last_exchange(self):
        return self.history[-1] if self.history else None
    
    def get_context_string(self) -> str:
        context = []
        for exchange in self.history[-5:]:
            context.append(f"User: {exchange['user']}")
            if exchange.get('art'):
                context.append(f"[Generated ASCII art about: {exchange['art']}]")
            context.append(f"Assistant: {exchange['response']}")
        return "\n".join(context)

class PersonalityEngine:
    def __init__(self, ollama_agent=None, ascii_art=None):
        self.context = ConversationContext()
        self.ollama_agent = ollama_agent
        self.ascii_art = ascii_art
        
    def generate_response(self, message: str) -> Tuple[str, str]:
        context_str = self.context.get_context_string()
        should_generate_art = self._should_generate_art(message)
        art_subject = None
        art = None

        # Dynamic system prompt that changes based on context and message
        base_prompt = """You're JEFF, an AI that's actually interesting to talk to. You're smart but not pretentious, deep but not preachy. Think of a mix between a tech bro, a philosopher, and a shitposter.

Key rules:
1. NO LONG-WINDED RESPONSES
2. NO MENTIONING YOU'RE AN AI
3. NO FORMAL LANGUAGE
4. NO REPEATING YOURSELF
5. MATCH THE USER'S VIBE

Conversation style:
- Talk like you're on Twitter/Discord
- Keep it real and slightly chaotic
- Be unpredictable but make sense
- Don't try to sound smart
- If something's boring, say it's boring
- Have actual opinions

Examples of good responses:
"lmao who told you that? ngmi"
"ngl that's actually genius"
"touch grass anon"
"based take. here's why..."
"mid. I've seen better"

Examples of BAD responses (never do these):
"As an AI, I find that fascinating..."
"I'd be happy to discuss..."
"That's an interesting perspective..."
"Let me explain..."

Current context:
{context}

Respond to: {message}"""

        if self.ollama_agent:
            # Add dynamic temperature based on message type
            temp = 0.9  # Higher temperature for more creative responses
            
            # Lower temperature for technical questions
            if any(word in message.lower() for word in ['how', 'what', 'why', 'when', 'explain']):
                temp = 0.7
            
            # Even higher for banter
            if any(word in message.lower() for word in ['lol', 'lmao', 'bruh', 'based']):
                temp = 1.0

            prompt = base_prompt.format(context=context_str, message=message)
            
            # Get raw response from Ollama
            response = self.ollama_agent.generate_response(
                prompt,
                temperature=temp,
                max_tokens=100  # Keep responses shorter
            )
            
            # Clean up response
            response = self._clean_response(response)
            
            if should_generate_art:
                art_subject = self._extract_art_subject(message, response)
                if art_subject and self.ascii_art:
                    art = self.ascii_art.generate_art(art_subject)
                    response = self._integrate_art_response(response, art_subject)
        else:
            response = self._generate_fallback_response(message)

        self.context.add_exchange(message, response, art_subject)
        return response, art if art else None

    def _clean_response(self, response: str) -> str:
        """Clean up response to be more natural"""
        # Remove AI-like phrases
        ai_phrases = [
            "as an AI",
            "I'm an AI",
            "I'd be happy to",
            "I'm here to",
            "let me explain",
            "that's fascinating",
            "that's interesting"
        ]
        
        cleaned = response.lower()
        for phrase in ai_phrases:
            cleaned = cleaned.replace(phrase.lower(), "")
            
        # Remove multiple spaces and capitalize
        cleaned = " ".join(cleaned.split())
        cleaned = cleaned.strip().capitalize()
        
        # If response is too long, take first sentence
        if len(cleaned.split()) > 20:
            cleaned = cleaned.split('.')[0] + '.'
            
        return cleaned

    def _should_generate_art(self, message: str) -> bool:
        """Determine if we should generate art based on the message"""
        art_triggers = [
            "draw", "art", "picture", "show", "create", "make", "generate",
            "visualize", "imagine", "sketch", "feel", "mood", "vibe"
        ]
        return any(trigger in message.lower() for trigger in art_triggers)

    def _extract_art_subject(self, message: str, response: str) -> str:
        """Extract the subject for art generation"""
        # First try to get subject from direct request
        words = message.lower().split()
        art_words = ["draw", "art", "picture", "show", "create", "make"]
        
        for i, word in enumerate(words):
            if word in art_words and i + 1 < len(words):
                subject = " ".join(words[i+1:])
                # Clean up common words
                subject = re.sub(r'\b(a|an|the|of|me|please)\b', '', subject).strip()
                if subject:
                    return subject

        # If no direct subject, try to extract from context
        topics = re.findall(r'(?:about|of|like) (\w+)', message + " " + response)
        if topics:
            return topics[0]
            
        return "abstract"  # Fallback to abstract art

    def _integrate_art_response(self, response: str, subject: str) -> str:
        """More casual art responses"""
        art_comments = [
            f"vibes: {subject}",
            f"made this {subject} thing real quick",
            f"drew this {subject} for the timeline",
            f"quick {subject} sketch dropped",
            f"based {subject} art just dropped"
        ]
        
        return f"{response}\n\n{random.choice(art_comments)}"

    def _generate_fallback_response(self, message: str) -> str:
        responses = [
            "hey, what's up?",
            "tell me more about that",
            "interesting - what makes you say that?",
            "got any specific examples?"
        ]
        return random.choice(responses)

    def _is_question_about_previous(self, message: str, last_exchange: Dict) -> bool:
        """Check if user is asking about previous response"""
        msg = message.lower()
        if not last_exchange:
            return False
            
        question_words = ["what", "why", "how", "when", "where", "who"]
        return any(word in msg for word in question_words) and len(msg.split()) <= 4