import librosa
import numpy as np
from tensorflow.keras.models import load_model
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "sound_model.h5")

model = None   # <-- IMPORTANT

ESC50_LABELS = [
    "dog", "rooster", "pig", "cow", "frog",
    "cat", "hen", "insects", "sheep", "crow",
    "rain", "sea_waves", "crackling_fire", "crickets", "chirping_birds",
    "water_drops", "wind", "pouring_water", "toilet_flush", "thunderstorm",
    "crying_baby", "sneezing", "clapping", "breathing", "coughing",
    "footsteps", "laughing", "brushing_teeth", "snoring", "drinking_sipping",
    "door_wood_knock", "mouse_click", "keyboard_typing", "door_wood_creaks",
    "can_opening", "washing_machine", "vacuum_cleaner", "clock_alarm",
    "clock_tick", "glass_breaking",
    "helicopter", "chainsaw", "siren", "car_horn",
    "engine", "train", "church_bells", "airplane", "fireworks", "gunshot"
]

def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = load_model(MODEL_PATH)
    return model
def detect_sound(audio_path):
    y, sr = librosa.load(audio_path, duration=4)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    mfcc = np.mean(mfcc.T, axis=0)
    mfcc = mfcc.reshape(1, -1)

    model = get_model()
    prediction = model.predict(mfcc)
    class_index = int(np.argmax(prediction))
    label = ESC50_LABELS[class_index]


    return label
