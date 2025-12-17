def extract_keywords(text):
    danger_words = ["help", "fire", "danger", "stop"]
    return [w for w in danger_words if w in text.lower()]
