import pytest
from src.agent.personality.engine import PersonalityEngine
from src.agent.personality.models import StyleCategory, Personality
import json
import os

@pytest.fixture
def test_personality_data():
    return {
        "name": "test_personality",
        "bio": ["Test bio 1", "Test bio 2"],
        "lore": ["Test lore 1", "Test lore 2"],
        "knowledge": ["Test knowledge 1", "Test knowledge 2"],
        "topics": ["AI", "technology", "crypto"],
        "style": {
            "all": ["uses emojis", "friendly tone"],
            "chat": ["direct responses", "helpful attitude"],
            "post": ["informative", "engaging"]
        },
        "adjectives": ["AMAZING", "INNOVATIVE"],
        "message_examples": [
            {
                "user": "test_user",
                "content": {
                    "text": "How does AI work?"
                }
            }
        ],
        "post_examples": [
            "🚀 Exciting developments in AI today!",
            "💡 New technology breakthrough!"
        ]
    }

@pytest.fixture
def setup_test_personality(test_personality_data, tmp_path):
    # Create temporary personality file
    personality_dir = tmp_path / "src/agent/personality/templates/test"
    personality_dir.mkdir(parents=True)
    
    with open(personality_dir / "personality.json", "w") as f:
        json.dump(test_personality_data, f)
    
    # Patch the base path in PersonalityEngine
    original_base_path = PersonalityEngine._load_personality.__defaults__[0]
    PersonalityEngine._load_personality.__defaults__ = (str(tmp_path / "src/agent/personality/templates"),)
    
    yield
    
    # Restore original base path
    PersonalityEngine._load_personality.__defaults__ = (original_base_path,)

def test_personality_initialization(setup_test_personality):
    engine = PersonalityEngine("test")
    assert engine.personality.name == "test_personality"
    assert len(engine.personality.topics) == 3
    assert "AI" in engine.personality.topics

def test_response_generation(setup_test_personality):
    engine = PersonalityEngine("test")
    context = {
        "user_id": "123",
        "original_message": "Tell me about AI",
        "context": "Previous discussion about technology"
    }
    
    response = engine.generate_response("How does AI work?", context)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_post_generation(setup_test_personality):
    engine = PersonalityEngine("test")
    post = engine.generate_post()
    assert post is not None
    assert isinstance(post, str)
    assert len(post) > 0

def test_style_application(setup_test_personality):
    engine = PersonalityEngine("test")
    message = "Tell me about technology"
    examples = engine._get_relevant_examples(message)
    
    styled_response = engine._apply_style(
        message=message,
        examples=examples,
        style_category=StyleCategory.CHAT
    )
    
    assert styled_response is not None
    assert isinstance(styled_response, str)

def test_error_handling(setup_test_personality):
    engine = PersonalityEngine("test")
    # Test with invalid message
    response = engine.generate_response(None)
    assert "I apologize" in response

def test_relevant_examples(setup_test_personality):
    engine = PersonalityEngine("test")
    examples = engine._get_relevant_examples("Tell me about AI")
    assert len(examples) > 0
    assert isinstance(examples, list)

def test_relevant_post_examples(setup_test_personality):
    engine = PersonalityEngine("test")
    examples = engine._get_relevant_post_examples("AI")
    assert len(examples) > 0
    assert isinstance(examples, list) 