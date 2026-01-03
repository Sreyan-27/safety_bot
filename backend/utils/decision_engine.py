from utils.memory import get_recent_events

def decide_action(
    sound_type="unknown",
    speech_text="",
    intent="normal",
    emotion="neutral",
    keywords=None,
    direction="unknown"
):
    # ----------------------------
    # Initialize decision object
    # ----------------------------
    decision = {
        "alert": False,
        "alert_level": "NONE",
        "threat_score": 0,
        "message": "",
        "context": {}
    }

    keywords = keywords or []

    # ----------------------------
    # Read short-term memory (STEP 3)
    # ----------------------------
    recent_events = get_recent_events(seconds=5)
    decision["context"]["recent_events"] = recent_events
    decision["context"]["direction"] = direction

    # ----------------------------
    # Threat scoring (STEP 4)
    # ----------------------------
    score = 0

    # Emotion impact
    if emotion in ["anger", "panic", "fear"]:
        score += 20

    # Sound impact
    if sound_type in ["scream", "vehicle", "horn", "gunshot"]:
        score += 30

    # Direction impact (something nearby)
    if direction in ["left", "right", "front"]:
        score += 10

    # Intent impact
    if intent in ["warning", "threat"]:
        score += 15

    # Keyword impact
    danger_keywords = {"help", "stop", "run", "danger", "save"}
    score += len(danger_keywords.intersection(set(keywords))) * 10

    # ----------------------------
    # Memory-based escalation
    # ----------------------------
    if len(recent_events) >= 5:
        score += 15

    # ----------------------------
    # Final decision
    # ----------------------------
    decision["threat_score"] = score

    if score >= 80:
        decision["alert"] = True
        decision["alert_level"] = "CRITICAL"
        decision["message"] = "Severe danger detected nearby"
    elif score >= 60:
        decision["alert"] = True
        decision["alert_level"] = "WARNING"
        decision["message"] = "Potential danger detected"
    else:
        decision["message"] = "Environment appears normal"

    return decision
