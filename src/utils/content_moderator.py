import re
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class ContentModerator:
    def __init__(self):
        # Add your own moderation rules
        self.blocked_patterns = [
            r'(?i)spam',
            r'(?i)abuse',
            r'(?i)hate',
            # Add more patterns
        ]
        
        self.max_length = 280  # Twitter's limit
        
    def check_content(self, content: str) -> Tuple[bool, str]:
        """
        Returns (is_safe, reason)
        """
        # Check length
        if len(content) > self.max_length:
            return False, "Content exceeds maximum length"
            
        # Check against blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, content):
                return False, f"Content matches blocked pattern: {pattern}"
                
        return True, ""
        
    def sanitize_content(self, content: str) -> str:
        """
        Clean up content before posting
        """
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        # Truncate if too long
        if len(content) > self.max_length:
            content = content[:self.max_length-3] + "..."
            
        return content 