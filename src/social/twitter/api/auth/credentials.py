import os
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class TwitterCredentials:
    bearer_token: str
    api_key: str
    api_secret: str
    access_token: str
    access_token_secret: str

def load_twitter_credentials() -> TwitterCredentials:
    load_dotenv()
    
    required_vars = [
        'TWITTER_BEARER_TOKEN',
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
    return TwitterCredentials(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        api_key=os.getenv('TWITTER_API_KEY'),
        api_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
