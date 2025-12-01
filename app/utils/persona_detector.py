"""Detect persona switch intent"""
import re
from typing import Optional
from app.services.agent.prompts import PERSONAS, DEFAULT_PERSONA
from app.core.logging import logger


def detect_persona_switch(message: str) -> Optional[str]:
    """
    Detect persona switch intent from user message.
    Returns the detected persona name if a switch is requested, None otherwise.
    Only returns a persona if the user explicitly requests a switch.
    """
    message_lower = message.lower()
    
    # Check for explicit persona switching phrases FIRST (highest priority)
    persona_patterns = {
        "mentor": r"act\s+(like|as)\s+(a\s+)?mentor|be\s+(my\s+)?mentor|switch\s+to\s+mentor|mentor\s+mode",
        "investor": r"act\s+(like|as)\s+(a\s+)?investor|be\s+(an\s+)?investor|switch\s+to\s+investor|investor\s+mode",
        "technical_advisor": r"act\s+(like|as)\s+(a\s+)?technical\s+(advisor|expert)|be\s+(a\s+)?technical\s+(advisor|expert)|switch\s+to\s+technical|technical\s+mode",
        "business_expert": r"act\s+(like|as)\s+(a\s+)?business\s+(expert|advisor)|be\s+(a\s+)?business\s+(expert|advisor)|switch\s+to\s+business|business\s+mode"
    }
    
    for persona, pattern in persona_patterns.items():
        if re.search(pattern, message_lower):
            logger.info(f"Detected {persona} persona via explicit pattern")
            return persona
    
    # Check for explicit persona mentions (lower priority, but still explicit)
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
    
    # Only check keywords if they appear in context that suggests a switch request
    # Look for phrases like "as a mentor", "like an investor", etc.
    if any(keyword in message_lower for keyword in mentor_keywords):
        # Check if it's in a switch context
        if any(phrase in message_lower for phrase in ["as a", "like a", "like an", "be my", "be a"]):
            logger.info("Detected mentor persona")
            return "mentor"
    
    if any(keyword in message_lower for keyword in investor_keywords):
        if any(phrase in message_lower for phrase in ["as a", "like a", "like an", "be my", "be an"]):
            logger.info("Detected investor persona")
            return "investor"
    
    if any(keyword in message_lower for keyword in technical_keywords):
        if any(phrase in message_lower for phrase in ["as a", "like a", "like an", "be my", "be a"]):
            logger.info("Detected technical_advisor persona")
            return "technical_advisor"
    
    if any(keyword in message_lower for keyword in business_keywords):
        if any(phrase in message_lower for phrase in ["as a", "like a", "like an", "be my", "be a"]):
            logger.info("Detected business_expert persona")
            return "business_expert"
    
    # Check for "back to" or "switch back" patterns
    back_to_patterns = {
        "mentor": r"back\s+to\s+(mentor|mentor\s+thread|mentor\s+mode)",
        "investor": r"back\s+to\s+(investor|investor\s+thread|investor\s+mode)",
        "technical_advisor": r"back\s+to\s+(technical|technical\s+thread|technical\s+mode|technical\s+advisor)",
        "business_expert": r"back\s+to\s+(business|business\s+thread|business\s+mode|business\s+expert)"
    }
    
    for persona, pattern in back_to_patterns.items():
        if re.search(pattern, message_lower):
            logger.info(f"Detected switch back to {persona} persona")
            return persona
    
    # No explicit switch detected - return None to continue current context
    logger.info("No persona switch detected, continuing current context")
    return None

