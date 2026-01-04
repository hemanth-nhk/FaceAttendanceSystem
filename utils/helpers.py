
def format_timestamp(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def log_event(message):
    log_file = "logs/app.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, "a") as f:
        f.write(f"[{format_timestamp(datetime.now())}] {message}\n")
from datetime import datetime
import os