from flask import Blueprint, request, jsonify

audio_bp = Blueprint("audio_bp", __name__)

@audio_bp.route("/analyze", methods=["POST"])
def analyze_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio uploaded"}), 400

    audio_file = request.files["audio"]

    # TODO: pass to ML model later
    return jsonify({
        "status": "processed",
        "intensity": "normal",
        "emergency_sound": "none",
        "keywords_detected": []
    })
