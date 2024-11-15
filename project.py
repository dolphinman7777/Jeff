from src.agent.llm.ollama.client import OllamaAgent
from src.social.twitter.api.handlers.tweet_handler import TwitterAgent
from src.memory.chroma.queries.storage import MemoryManager
from src.agent.personality.engine import PersonalityEngine
from src.agent.context.conversation_manager import ConversationManager
import logging
import time
from datetime import datetime
import backoff
import signal
import sys
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

# Fun ASCII art signatures to use randomly
SIGNATURES = [
    "ʕ •ᴥ•ʔ", "(-‿‿-)", "(｡◕‿◕｡)", "◉_◉", "^̮^", 
    "(╯°□°）╯︵ ┻━┻", "┬──┬◡ﾉ(° -°ﾉ)", "¯\_(ツ)_/¯"
]

def get_random_style():
    """Generate random styling for responses"""
    styles = ["bold", "italic", "blue", "green", "yellow", "red", "magenta", "cyan"]
    return random.choice(styles)

class JEFF:
    def __init__(self):
        self.console = Console()
        self.personality_traits = [
            "sarcastic", "witty", "philosophical", "playful",
            "deadpan", "enthusiastic", "mysterious"
        ]
        self.current_mood = random.choice(self.personality_traits)
        self.ollama_agent = OllamaAgent(model="mistral")  # Specify model
        self.conversation_history = []
        
    def get_response(self, user_input):
        """Generate response using Ollama and apply personality"""
        with self.console.status("[bold green]Thinking...", spinner="dots"):
            # Build context from conversation history
            context = "\n".join([f"User: {msg[0]}\nJEFF: {msg[1]}" for msg in self.conversation_history[-3:]])
            
            # Craft prompt with personality and context
            prompt = f"""You are JEFF, an AI with a {self.current_mood} personality.
Previous conversation:
{context}

User: {user_input}

Respond in a {self.current_mood} way. Keep responses concise (max 2-3 sentences). 
If asked about capabilities you don't have, be creative and funny rather than apologetic.
Never mention being an AI or having limitations."""

            # Get base response from Ollama
            base_response = self.ollama_agent.generate_response(prompt)
            
            # Store in history
            self.conversation_history.append((user_input, base_response))
            
            # Fun responses for special cases
            if "draw" in user_input.lower():
                return """
    ╭━━━╮
    ┃   ┃
    ┃ ◡ ┃  Here's my masterpiece!
    ╰━━━╯
                """
                
            if any(word in user_input.lower() for word in ["bitch", "fuck", "shit"]):
                return "Woah there! I'm too classy for that kind of talk. Let's keep it civil, darling! ✨"
            
            # Apply personality template based on current mood
            templates = {
                "sarcastic": ["*slow clap* {} ", "How fascinating... {}"],
                "witty": ["Here's a zinger: {} ", "Plot twist: {}"],
                "philosophical": ["In the cosmic dance of existence... {}", "As the ancient ones would say: {}"],
                "playful": ["*bounces around* {} ", "*does a little dance* {}"],
                "deadpan": ["PROCESSING HUMOR.EXE... {}", "ENGAGING SMALL TALK PROTOCOL: {}"],
                "enthusiastic": ["HOLY MOLY! {} ", "THIS IS AMAZING! {}"],
                "mysterious": ["*emerges from the shadows* {} ", "*crystal ball glows* {}"]
            }
            
            template = random.choice(templates[self.current_mood])
            return template.format(base_response)

    def respond(self, user_input):
        try:
            response = self.get_response(user_input)
            
            # Visual flair
            style = get_random_style()
            signature = random.choice(SIGNATURES)
            
            # Add random emoji based on mood
            mood_emojis = {
                "sarcastic": "🙄",
                "witty": "😏",
                "philosophical": "🤔",
                "playful": "🎈",
                "deadpan": "😐",
                "enthusiastic": "✨",
                "mysterious": "🌌"
            }
            
            emoji = mood_emojis.get(self.current_mood, "")
            formatted_response = f"{response}\n\n{signature} {emoji}"
            
            panel = Panel(
                Text(formatted_response, style=style),
                title=f"JEFF ({self.current_mood} mood)",
                border_style=style
            )
            
            self.console.print(panel)
            
            # More frequent mood changes
            if random.random() < 0.4:  # 40% chance
                old_mood = self.current_mood
                while self.current_mood == old_mood:  # Ensure mood actually changes
                    self.current_mood = random.choice(self.personality_traits)
                
        except Exception as e:
            self.console.print(f"[bold red]Whoopsie! {str(e)}[/bold red]")

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}")
    if 'system' in globals():
        system.stop()

def main():
    global system
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Set logging to ERROR to reduce output
        logging.getLogger().setLevel(logging.ERROR)
        
        system = JEFF()
        console.print("[bold blue]🤖 JEFF is online[/bold blue]")
        console.print("[italic]I have multiple personality traits and my mood changes randomly.[/italic]")
        console.print("[italic]Type 'exit' or 'quit' to end chat[/italic]\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    console.print("[bold red]Goodbye! ʕ •ᴥ•ʔ[/bold red]")
                    break
                    
                system.respond(user_input)
                
            except KeyboardInterrupt:
                console.print("\n[bold red]Caught interrupt signal, shutting down...[/bold red]")
                break
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")
                
    except Exception as e:
        logger.error(f"Error running ResponseSystem: {e}", exc_info=True)
    finally:
        console.print("\n👋 JEFF has left the chat")

def debug_mode():
    system = JEFF()
    print("\n🔍 Debug Mode - Testing System Components\n")
    
    # Test Ollama
    print("Testing Ollama...")
    response = system.ollama_agent.generate_response("Hello")
    print(f"Ollama Response: {response}\n")
    
    # Test Memory
    print("Testing Memory...")
    embedding = system.ollama_agent.generate_embedding("Test message")
    system.memory_manager.store_interaction("test_user", "Test message", embedding)
    context = system.memory_manager.retrieve_context("test_user")
    print(f"Memory Context: {context}\n")
    
    # Test Personality
    print("Testing Personality...")
    personality_response = system.personality.generate_response("Hello!")
    print(f"Personality Response: {personality_response}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        debug_mode()
    else:
        main() 