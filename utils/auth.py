import json
import bcrypt
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}  # Return empty dict if file does not exist
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def authenticate_user(username, password):
    users = load_users()
    print("[DEBUG] Users Loaded:", users)

    if username in users:
        stored_hash = users[username]
        print(f"[DEBUG] Stored hash for {username}: {stored_hash}")
        result = bcrypt.checkpw(password.encode(), stored_hash.encode())
        print(f"[DEBUG] Password check result: {result}")
        return result

    print("[DEBUG] Username not found")
    return False

def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # User already exists
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = hashed_pw.decode()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    return True
