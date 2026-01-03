import time
from collections import deque

# store last N events
EVENT_MEMORY = deque(maxlen=10)

def add_event(event_type, data):
    EVENT_MEMORY.append({
        "type": event_type,
        "data": data,
        "timestamp": time.time()
    })

def get_recent_events(seconds=5):
    now = time.time()
    return [
        e for e in EVENT_MEMORY
        if now - e["timestamp"] <= seconds
    ]
