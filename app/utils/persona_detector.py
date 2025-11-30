"""Detect persona switch intent"""
import re
from app.services.agent.prompts import PERSONAS, DEFAULT_PERSONA
from app.core.logging import logger


def detect_persona_switch(message: str) -> str:
    """
    Detect persona switch intent from user message.
    Returns the detected persona name.
    """
    message_lower = message.lower()
    
    # Keywords for each persona
    mentor_keywords = [
        "mentor", "guide me", "advice", "help me learn", "teach me",
        "support", "coach", "guidance"
    ]
    
    investor_keywords = [
        "investor", "investment", "roi", "return on investment",
        "market size", "unit economics", "valuation", "funding",
        "pitch", "business case"
    ]
    
    technical_keywords = [
        "technical", "code", "implementation", "architecture",
        "system design", "algorithm", "programming", "tech stack",
        "api", "database", "infrastructure"
    ]
    
    business_keywords = [
        "business", "strategy", "market", "competition", "revenue",
        "growth", "operations", "business model", "go-to-market"
    ]
    
    # Check for explicit persona mentions first
    if any(keyword in message_lower for keyword in mentor_keywords):
        logger.info("Detected mentor persona")
        return "mentor"
    
    if any(keyword in message_lower for keyword in investor_keywords):
        logger.info("Detected investor persona")
        return "investor"
    
    if any(keyword in message_lower for keyword in technical_keywords):
        logger.info("Detected technical_advisor persona")
        return "technical_advisor"
    
    if any(keyword in message_lower for keyword in business_keywords):
        logger.info("Detected business_expert persona")
        return "business_expert"
    
    # Check for explicit persona switching phrases
    persona_patterns = {
        "mentor": r"act\s+(like|as)\s+(a\s+)?mentor",
        "investor": r"act\s+(like|as)\s+(a\s+)?investor",
        "technical_advisor": r"act\s+(like|as)\s+(a\s+)?technical\s+(advisor|expert)",
        "business_expert": r"act\s+(like|as)\s+(a\s+)?business\s+(expert|advisor)"
    }
    
    for persona, pattern in persona_patterns.items():
        if re.search(pattern, message_lower):
            logger.info(f"Detected {persona} persona via explicit pattern")
            return persona
    
    # Default to business_expert
    logger.info(f"No persona detected, using default: {DEFAULT_PERSONA}")
    return DEFAULT_PERSONA

