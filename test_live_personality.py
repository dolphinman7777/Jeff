from src.agent.personality.engine import PersonalityEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_live_personality():
    try:
        # Initialize personality engine
        engine = PersonalityEngine("default")
        
        # Test response generation
        test_messages = [
            "Tell me about AI",
            "What's happening with crypto?",
            "How does this work?",
            "Hello!"
        ]
        
        logger.info("Testing response generation...")
        for message in test_messages:
            context = {
                "user_id": "test_user",
                "original_message": message,
                "context": "First interaction"
            }
            
            response = engine.generate_response(message, context)
            logger.info(f"\nInput: {message}\nResponse: {response}\n")
        
        # Test post generation
        logger.info("Testing post generation...")
        for _ in range(3):
            post = engine.generate_post()
            logger.info(f"Generated post: {post}\n")
            
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    test_live_personality() 