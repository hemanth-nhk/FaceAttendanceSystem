from utils.auth import register_user

username = input("Enter new username: ")
password = input("Enter new password: ")

if register_user(username, password):
    print("✅ User registered successfully.")
else:
    print("❌ User already exists.")
