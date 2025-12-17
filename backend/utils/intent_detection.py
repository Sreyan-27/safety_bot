def detect_intent(text):
    if any(word in text.lower() for word in ["stop", "move", "careful", "run"]):
        return "warning"
    if "help" in text.lower():
        return "help"
    return "normal"
