import wave
import numpy as np

def detect_direction(audio_path):
    """
    Detects approximate sound direction using stereo balance.
    Returns: left / right / front
    """

    with wave.open(audio_path, 'rb') as wf:
        if wf.getnchannels() != 2:
            return "unknown"

        frames = wf.readframes(wf.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

        left = audio[0::2]
        right = audio[1::2]

        left_energy = np.mean(np.abs(left))
        right_energy = np.mean(np.abs(right))

        if left_energy > right_energy * 1.1:
            return "left"
        elif right_energy > left_energy * 1.1:
            return "right"
        else:
            return "front"
