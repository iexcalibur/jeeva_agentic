"""Tests for agent service"""
import pytest
from app.services.agent.prompts import PERSONAS, DEFAULT_PERSONA
from app.utils.persona_detector import detect_persona_switch


def test_persona_detection_mentor():
    """Test mentor persona detection"""
    message = "Act like my mentor and help me with product strategy"
    persona = detect_persona_switch(message)
    assert persona == "mentor"


def test_persona_detection_investor():
    """Test investor persona detection"""
    message = "I need investment advice on my startup"
    persona = detect_persona_switch(message)
    assert persona == "investor"


def test_persona_detection_technical():
    """Test technical advisor persona detection"""
    message = "Help me with the technical implementation"
    persona = detect_persona_switch(message)
    assert persona == "technical_advisor"


def test_persona_detection_default():
    """Test default persona when no match"""
    message = "Hello, how are you?"
    persona = detect_persona_switch(message)
    assert persona == DEFAULT_PERSONA

