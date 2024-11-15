from dataclasses import dataclass
from typing import List, Dict, Optional
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StyleCategory(Enum):
    ALL = "all"
    CHAT = "chat"
    POST = "post"

@dataclass
class PersonalityStyle:
    all: List[str]
    chat: List[str]
    post: List[str]

    @classmethod
    def from_dict(cls, data: Dict) -> 'PersonalityStyle':
        return cls(
            all=data.get('all', []),
            chat=data.get('chat', []),
            post=data.get('post', [])
        )

@dataclass
class Personality:
    name: str
    bio: List[str]
    lore: List[str]
    knowledge: List[str]
    topics: List[str]
    style: PersonalityStyle
    adjectives: List[str]
    message_examples: List[Dict]
    post_examples: List[str]

    @classmethod
    def from_dict(cls, data: Dict) -> 'Personality':
        return cls(
            name=data.get('name', ''),
            bio=data.get('bio', []),
            lore=data.get('lore', []),
            knowledge=data.get('knowledge', []),
            topics=data.get('topics', []),
            style=PersonalityStyle.from_dict(data.get('style', {})),
            adjectives=data.get('adjectives', []),
            message_examples=data.get('message_examples', []),
            post_examples=data.get('post_examples', [])
        ) 