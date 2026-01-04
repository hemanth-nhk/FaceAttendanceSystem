
import boto3
import os

def upload_to_s3(file_path, bucket_name, object_name=None):
    s3 = boto3.client('s3')
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print("Upload Successful")
        return True
    except Exception as e:
        print("Upload failed:", e)
        return False

# === STEP 9: Login Authentication: utils/auth.py ===
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "admin": hash_password("admin123")
}

def verify_login(username, password):
    if username in USERS and USERS[username] == hash_password(password):
        return True
    return False
import boto3
import os
from datetime import datetime

def upload_to_s3():
    today = datetime.now().strftime('%Y-%m-%d')
    file_path = f'reports/attendance_{today}.csv'
    if not os.path.exists(file_path):
        print("No report to upload.")
        return

    s3 = boto3.client('s3',
                      aws_access_key_id='YOUR_ACCESS_KEY',
                      aws_secret_access_key='YOUR_SECRET_KEY')
    s3.upload_file(file_path, 'your-bucket-name', f'attendance/{os.path.basename(file_path)}')
    print("Uploaded to S3.")
