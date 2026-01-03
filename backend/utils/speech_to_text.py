from vosk import Model, KaldiRecognizer
import wave
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOSK_MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15")

model = None

def get_stt_model():
    global model
    if model is None:
        model = Model(VOSK_MODEL_PATH)
    return model


def speech_to_text(audio_path):
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(get_stt_model(), wf.getframerate())

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result += json.loads(rec.Result()).get("text", "")

    result += json.loads(rec.FinalResult()).get("text", "")
    return result.strip()
