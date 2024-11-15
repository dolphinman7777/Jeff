import logging
from typing import Optional
import tweepy
import time
from src.social.twitter.api.auth.credentials import load_twitter_credentials
from src.utils.rate_limiter import RateLimiter, RateLimit
from src.utils.content_moderator import ContentModerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterAgent:
    def __init__(self):
        self.credentials = load_twitter_credentials()
        self.api = self._init_api()
        self.rate_limiter = RateLimiter({
            'tweets': RateLimit(max_requests=50, time_window=3600),  # Reduced limits
            'mentions': RateLimit(max_requests=15, time_window=900)
        })
        self.moderator = ContentModerator()
        logger.info("Initialized TwitterAgent")

    def _init_api(self) -> tweepy.Client:
        try:
            client = tweepy.Client(
                bearer_token=self.credentials.bearer_token,
                consumer_key=self.credentials.api_key,
                consumer_secret=self.credentials.api_secret,
                access_token=self.credentials.access_token,
                access_token_secret=self.credentials.access_token_secret,
                wait_on_rate_limit=True  # Add automatic rate limit handling
            )
            # Verify credentials
            me = client.get_me()
            logger.info(f"Authenticated as: {me.data.username}")
            return client
        except Exception as e:
            logger.error(f"Error initializing Twitter API: {e}")
            raise

    def _handle_rate_limit(self, e: Exception) -> bool:
        if hasattr(e, 'response') and e.response.status_code == 429:
            reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
            if reset_time:
                wait_time = reset_time - int(time.time()) + 1
                if wait_time > 0:
                    logger.info(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    return True
        return False

    def post_tweet(self, content: str, reply_to: Optional[str] = None) -> bool:
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if not self.rate_limiter.check_rate_limit('tweets'):
                    logger.warning("Local rate limit exceeded, waiting...")
                    time.sleep(60)
                    continue
                
                # Moderate content
                is_safe, reason = self.moderator.check_content(content)
                if not is_safe:
                    logger.warning(f"Content moderation failed: {reason}")
                    return False
                
                # Sanitize content
                content = self.moderator.sanitize_content(content)
                
                response = self.api.create_tweet(
                    text=content,
                    in_reply_to_tweet_id=reply_to
                )
                logger.info(f"Successfully posted tweet: {content[:50]}...")
                return True
                
            except Exception as e:
                logger.warning(f"Error posting tweet (attempt {retry_count + 1}): {e}")
                if self._handle_rate_limit(e):
                    continue
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error("Max retries exceeded")
                    return False
                time.sleep(5 * retry_count)  # Exponential backoff
        
        return False

    def get_mentions(self, since_id: Optional[str] = None) -> list:
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if not self.rate_limiter.check_rate_limit('mentions'):
                    logger.warning("Local rate limit exceeded, waiting...")
                    time.sleep(60)
                    continue
                
                mentions = self.api.get_users_mentions(
                    id=self.api.get_me().data.id,
                    since_id=since_id,
                    max_results=10  # Limit results per request
                )
                return mentions.data or []
                
            except Exception as e:
                logger.warning(f"Error fetching mentions (attempt {retry_count + 1}): {e}")
                if self._handle_rate_limit(e):
                    continue
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error("Max retries exceeded")
                    return []
                time.sleep(5 * retry_count)
        
        return []
