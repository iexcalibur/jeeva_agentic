"""Claude API wrapper"""
from langchain_anthropic import ChatAnthropic
from app.core.config import settings
from app.core.logging import logger


def create_claude_llm(temperature: float = 0.7) -> ChatAnthropic:
    """Create and configure Claude LLM instance"""
    try:
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )
        logger.info("Claude LLM instance created successfully")
        return llm
    except Exception as e:
        logger.error(f"Failed to create Claude LLM: {str(e)}")
        raise

