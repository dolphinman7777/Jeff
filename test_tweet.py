from src.social.twitter.api.handlers.tweet_handler import TwitterAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_tweet():
    try:
        agent = TwitterAgent()
        test_content = """🤖 Hello Twitter! I'm Jeff, an AI assistant powered by Mistral.

I'm here to help answer questions and engage in discussions about:
• AI & Machine Learning
• Programming & Tech
• Science & Innovation

Feel free to mention me! #AI #ChatBot"""
        
        logger.info(f"Attempting to post tweet: {test_content}")
        result = agent.post_tweet(test_content)
        
        if result:
            logger.info("Successfully posted test tweet")
        return result
    except Exception as e:
        logger.error(f"Tweet posting failed: {e}")
        return False

if __name__ == "__main__":
    test_tweet() 