import json
from datetime import datetime

def log(event_type, payload):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "payload": payload,
    }
    print(json.dumps(entry))