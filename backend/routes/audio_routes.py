from flask import Blueprint, request, jsonify
import os
import uuid

# Utils
from utils.audio_processing import detect_sound
from utils.keyword_detection import extract_keywords
from utils.alerting import send_alert
from utils.memory import add_event
from utils.direction_detection import detect_direction
from utils.speech_to_text import speech_to_text
from utils.emotion_detection import detect_emotion
from utils.intent_detection import detect_intent

# Brain
from utils.decision_engine import decide_action

audio_bp = Blueprint("audio", __name__)

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@audio_bp.route("/analyze", methods=["POST"])
def analyze_audio():
    # 1️⃣ Validate request
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    # 2️⃣ Save audio
    filename = f"{uuid.uuid4()}.wav"
    audio_path = os.path.join(UPLOAD_DIR, filename)
    audio_file.save(audio_path)

    # 3️⃣ Audio intelligence
    sound_type = detect_sound(audio_path)
    direction = detect_direction(audio_path)

    # 4️⃣ Speech intelligence
    speech_text = speech_to_text(audio_path)
    emotion = detect_emotion(speech_text)
    intent = detect_intent(speech_text)
    keywords = extract_keywords(speech_text)

    # 5️⃣ Short-term memory (STEP 2)
    add_event("sound", sound_type)
    add_event("direction", direction)
    add_event("speech", speech_text)
    add_event("emotion", emotion)
    add_event("intent", intent)

    # 6️⃣ Decision engine (brain)
    decision = decide_action(
        sound_type=sound_type,
        speech_text=speech_text,
        intent=intent,
        emotion=emotion,
        keywords=keywords,
        direction=direction
    )

    # 7️⃣ Alert if needed
    if decision.get("alert"):
        send_alert(decision)

    # 8️⃣ Cleanup temp file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    # 9️⃣ Response
    return jsonify({
        "sound_type": sound_type,
        "direction": direction,
        "speech_text": speech_text,
        "emotion": emotion,
        "intent": intent,
        "keywords": keywords,
        "decision": decision
    })
