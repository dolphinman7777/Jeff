from src.social.twitter.api.handlers.tweet_handler import TwitterAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_twitter_connection():
    try:
        agent = TwitterAgent()
        me = agent.api.get_me()
        logger.info(f"Successfully connected as: {me.data.username}")
        return True
    except Exception as e:
        logger.error(f"Twitter connection failed: {e}")
        return False

if __name__ == "__main__":
    test_twitter_connection() 