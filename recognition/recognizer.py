
import face_recognition
import cv2
import os
import numpy as np
from datetime import datetime
from database.models import init_db, Attendance

Session = init_db()

# Preload known face encodings and names
known_face_encodings = []
known_face_names = []

data_path = 'data/'

for filename in os.listdir(data_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(data_path, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

def mark_attendance(frame):
    session = Session()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    name = "Unknown"

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

            existing = session.query(Attendance).filter_by(name=name).order_by(Attendance.timestamp.desc()).first()
            now = datetime.now()
            if not existing or (now - existing.timestamp).total_seconds() > 60:
                attendance = Attendance(name=name, timestamp=now, status='Present')
                session.add(attendance)
                session.commit()

    return name

import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pandas as pd

KNOWN_FACES_DIR = 'data'
ATTENDANCE_FILE = 'reports/attendance.csv'

known_encodings = []
known_names = []

# Load known faces
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])

def mark_attendance(name):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
        df.to_csv(ATTENDANCE_FILE, index=False)
    df = pd.read_csv(ATTENDANCE_FILE)
    if not ((df['Name'] == name) & (df['Date'] == date)).any():
        new_entry = pd.DataFrame([[name, date, time]], columns=["Name", "Date", "Time"])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)


def run_recognition():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for encoding, loc in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            if matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    mark_attendance(name)

            top, right, bottom, left = [v * 4 for v in loc]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Attendance System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()