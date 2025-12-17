from utils.speech_to_text import speech_to_text
from utils.intent_detection import detect_intent
from utils.emotion_detection import detect_emotion
from utils.keyword_detection import extract_keywords
from core.decision_engine import decide_action
from utils.alerting import trigger_alert
from utils.direction_detection import detect_direction

@audio_bp.route('/analyze', methods=['POST'])
def analyze_audio():
    # 1️⃣ Get audio from user
    audio_file = request.files['audio']
    audio_path = "temp.wav"
    audio_file.save(audio_path)

    # 2️⃣ Convert speech → text
    text = speech_to_text(audio_path)

    # 3️⃣ Understand the text
    intent = detect_intent(text)
    emotion = detect_emotion(text)
    keywords = extract_keywords(text)

    # 4️⃣ Decide what to do (brain)
    decision = decide_action(
        sound_type="unknown",
        speech_text=text,
        intent=intent,
        emotion=emotion,
        keywords=keywords,
        confidence=0.85
    )

    # 5️⃣ React if needed
    if decision["alert"]:
        trigger_alert(decision)

    # 6️⃣ Send response back
    return jsonify({
    "speech": text,
    "intent": intent,
    "emotion": emotion,
    "keywords": keywords,
    "direction": direction,
    "decision": decision
     })

