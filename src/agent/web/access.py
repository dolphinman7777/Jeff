import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

class WebAccess:
    def __init__(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.session = requests.Session()
        
    def get_weather(self, location: str = "London") -> Dict[str, Any]:
        """Get current weather for location"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}"
            response = self.session.get(url)
            return response.json()
        except Exception as e:
            self.logger.error(f"Weather API error: {e}")
            return {"error": str(e)}

    def get_news(self, topic: str = "technology") -> Dict[str, Any]:
        """Get latest news about topic"""
        try:
            url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={self.news_api_key}"
            response = self.session.get(url)
            return response.json()
        except Exception as e:
            self.logger.error(f"News API error: {e}")
            return {"error": str(e)}

    def search_wikipedia(self, query: str) -> Optional[str]:
        """Search Wikipedia for information"""
        try:
            url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "titles": query
            }
            response = self.session.get(url, params=params)
            data = response.json()
            pages = data["query"]["pages"]
            return next(iter(pages.values()))["extract"]
        except Exception as e:
            self.logger.error(f"Wikipedia API error: {e}")
            return None 