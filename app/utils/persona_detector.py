"""Detect persona switch intent"""
import re
from typing import Optional
from app.core.logging import logger


def detect_persona_switch(message: str) -> Optional[str]:
    """
    Detect persona switch intent from user message.
    Returns the detected persona name if a switch is requested, None otherwise.
    
    Priorities:
    1. Explicit Commands ("Act like a mentor")
    2. Contextual Switches ("Back to mentor")
    3. Intent/Topic Detection ("I need investment advice")
    """
    message_lower = message.lower()
    
    # --- 1. Explicit Commands (Highest Priority) ---
    # Flexible Pattern:
    # 1. Starts with command verb (act, be, switch)
    # 2. Allows any number of filler words (like, as, to, a, my, the, skeptical, etc.)
    # 3. Ends with the persona name
    
    # Matches: "Act my mentor", "Act like a mentor", "Be investor", "Switch to tech", "Act like a skeptical investor"
    base_pattern = r"\b(?:act|be|switch)(?:\s+(?:like|as|to|a|an|the|my|your|skeptical|supportive|technical))*\s+"

    persona_patterns = {
        "mentor": f"{base_pattern}mentor\\b|mentor\\s+mode",
        "investor": f"{base_pattern}investor\\b|investor\\s+mode",
        # Technical often has two words like "technical advisor" or just "technical"
        "technical_advisor": f"{base_pattern}(?:technical|tech)\\b|technical\\s+mode",
        "business_expert": f"{base_pattern}business\\b|business\\s+mode"
    }
    
    for persona, pattern in persona_patterns.items():
        if re.search(pattern, message_lower):
            logger.info(f"Detected {persona} persona via explicit pattern")
            return persona

    # --- 2. "Switch Back" Context (Medium Priority) ---
    # Matches: "back to mentor", "previous thread", "return to investor"
    if "back to" in message_lower or "return to" in message_lower:
        if "mentor" in message_lower: 
            logger.info("Detected switch back to mentor")
            return "mentor"
        if "investor" in message_lower: 
            logger.info("Detected switch back to investor")
            return "investor"
        if "technical" in message_lower or "tech" in message_lower: 
            logger.info("Detected switch back to technical_advisor")
            return "technical_advisor"
        if "business" in message_lower: 
            logger.info("Detected switch back to business_expert")
            return "business_expert"

    # --- 3. Intent-Based Detection (Smart Switching) ---
    # Matches topics without explicit commands: "I need investment advice", "help me with code"
    
    # Investor Intents: funding, roi, pitch deck, investment advice
    # \b ensures we match whole words (e.g., avoiding "android" matching "roi")
    if re.search(r"\b(investment|funding|valuation|pitch deck|roi|unit economics|investor|cap table|term sheet)\b", message_lower):
        logger.info("Detected investor persona via Intent")
        return "investor"

    # Technical Intents: code, python, api, db, architecture
    # Filter out generic business usage of "tech" if possible, but prioritize technical keywords
    if re.search(r"\b(code|python|typescript|java|react|api|database|aws|docker|bug|error|exception|stack trace|algorithm|system design)\b", message_lower):
        # Optional: prevent false positives if the user is asking about the "business of tech"
        if not re.search(r"\b(market size|revenue|sales|marketing)\b", message_lower): 
            logger.info("Detected technical_advisor persona via Intent")
            return "technical_advisor"

    # Mentor Intents: learn, teach, guide, roadmap
    if re.search(r"\b(learn|teach|guide|roadmap|career|study|how to learn|curriculum|syllabus)\b", message_lower):
        logger.info("Detected mentor persona via Intent")
        return "mentor"

    # No explicit switch detected - return None to continue current context
    logger.info("No persona switch detected, continuing current context")
    return None