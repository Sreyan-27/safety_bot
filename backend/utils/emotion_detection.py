def detect_emotion(text):
    if any(word in text.lower() for word in ["panic", "scared", "fear"]):
        return "panic"
    return "neutral"
