"""
Decision Engine
----------------
This module acts like the human brain.
It combines sound, speech, emotion, intent, and keywords
to decide whether to alert the user and how urgent it is.
"""
from utils.memory import get_recent_events

def decide_action(
    sound_type="unknown",
    speech_text="",
    intent="normal",
    emotion="neutral",
    keywords=None,
    direction="unknown"
):
    decision = {
        "alert": False,
        "alert_level": "NONE",
        "message": "",
        "context": {}
    }

    decision["context"]["direction"] = direction
    
    # Initialize
    keywords = keywords or []
    score = 0.0

    # ----------------------------
    # Priority Scoring Logic
    # ----------------------------

    # 1. Intent-based scoring
    if intent == "warning":
        score += 0.3
    elif intent == "help":
        score += 0.4

    # 2. Emotion-based scoring
    if emotion in ["panic", "fear"]:
        score += 0.2
    elif emotion == "stress":
        score += 0.1

    # 3. Keyword-based scoring
    emergency_keywords = ["help", "fire", "danger", "stop", "run"]
    if any(word in emergency_keywords for word in keywords):
        score += 0.4

    # 4. Sound-based scoring
    if sound_type in ["vehicle", "horn", "scream"]:
        score += 0.3

    # ----------------------------
    # Alert Level Decision
    # ----------------------------
    if score >= 0.8:
        alert_level = "CRITICAL"
    elif score >= 0.5:
        alert_level = "HIGH"
    elif score >= 0.3:
        alert_level = "MEDIUM"
    else:
        alert_level = "LOW"

    # ----------------------------
    # Final Decision Object
    # ----------------------------
    decision = {
        "alert": score >= 0.3,
        "priority_score": round(score, 2),
        "alert_level": alert_level,
        "context": {
            "sound_type": sound_type,
            "speech_text": speech_text,
            "intent": intent,
            "emotion": emotion,
            "keywords": keywords
        }
    }

    return decision
