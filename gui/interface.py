import os
import cv2
import csv
import face_recognition
from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore
import pandas as pd


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, student_name=None):
        super().__init__()
        self.setWindowTitle("Attendance System - Face Recognition")
        self.setGeometry(100, 100, 1000, 700)
        self.student_name = student_name
        self.cap = None
        self.timer = None
        self.frame_count = 0
        self.logged_names = set()
        self.known_face_encodings = []
        self.known_face_names = []
        self.setup_ui()
        self.load_known_faces()

    def setup_ui(self):
        # Main layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QtWidgets.QVBoxLayout(central_widget)

        # Menu Bar
        menu_bar = self.menuBar()
        session_menu = menu_bar.addMenu("Session")

        logout_action = QtWidgets.QAction("Logout", self)
        logout_action.triggered.connect(self.handle_logout)
        session_menu.addAction(logout_action)

        back_action = QtWidgets.QAction("Go Back to Login", self)
        back_action.triggered.connect(self.handle_go_back)
        session_menu.addAction(back_action)

        # Welcome
        welcome_label = QtWidgets.QLabel(f"Welcome {self.student_name or 'User'}")
        welcome_label.setFont(QtGui.QFont("Arial", 16))
        welcome_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(welcome_label)

        # Video Display
        self.video_label = QtWidgets.QLabel()
        self.video_label.setFixedHeight(480)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.video_label)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()

        self.recognition_btn = QtWidgets.QPushButton("Start Face Recognition")
        self.recognition_btn.setStyleSheet("background-color: green; color: white; padding: 8px;")
        self.recognition_btn.clicked.connect(self.toggle_recognition)
        btn_layout.addWidget(self.recognition_btn)

        export_csv_btn = QtWidgets.QPushButton("Export to CSV")
        export_csv_btn.setStyleSheet("background-color: #3b5998; color: white; padding: 8px;")
        export_csv_btn.clicked.connect(self.export_csv)
        btn_layout.addWidget(export_csv_btn)

        export_excel_btn = QtWidgets.QPushButton("Export to Excel")
        export_excel_btn.setStyleSheet("background-color: #d9534f; color: white; padding: 8px;")
        export_excel_btn.clicked.connect(self.export_excel)
        btn_layout.addWidget(export_excel_btn)

        self.layout.addLayout(btn_layout)

        self.status = QtWidgets.QLabel("")
        self.layout.addWidget(self.status)

    def load_known_faces(self):
        dataset_path = os.path.join(os.path.dirname(__file__), '..', 'faces')
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

        for person_name in os.listdir(dataset_path):
            person_dir = os.path.join(dataset_path, person_name)
            if os.path.isdir(person_dir):
                for img_name in os.listdir(person_dir):
                    img_path = os.path.join(person_dir, img_name)
                    image = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(person_name)

    def toggle_recognition(self):
        if self.cap and self.cap.isOpened():
            self.timer.stop()
            self.cap.release()
            self.video_label.clear()
            self.recognition_btn.setText("Start Face Recognition")
            self.status.setText("[INFO] Recognition stopped.")
        else:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.status.setText("[ERROR] Cannot access webcam.")
                return
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)
            self.frame_count = 0
            self.logged_names.clear()
            self.recognition_btn.setText("Stop Face Recognition")
            self.status.setText("[INFO] Recognition started.")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.status.setText("[ERROR] Failed to grab frame.")
            return

        self.frame_count += 1
        if self.frame_count % 5 != 0:
            return

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            name = "Unknown"
            if self.known_face_encodings:
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = distances.argmin()
                if distances[best_match_index] < 0.45:
                    name = self.known_face_names[best_match_index]

            if name != "Unknown" and name not in self.logged_names:
                self.log_attendance(name)
                self.logged_names.add(name)

            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        qt_img = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap.fromImage(qt_img)
        self.video_label.setPixmap(pixmap)

    def log_attendance(self, name):
        log_file = os.path.join(os.path.dirname(__file__), '..', 'attendance.csv')
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        if not os.path.exists(log_file):
            with open(log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Timestamp'])

        with open(log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, timestamp])
        self.status.setText(f"[INFO] Logged attendance for {name}")

    def export_csv(self):
        self.status.setText("[INFO] Attendance already in CSV format.")

    def export_excel(self):
        csv_file = os.path.join(os.path.dirname(__file__), '..', 'attendance.csv')
        excel_file = os.path.join(os.path.dirname(__file__), '..', 'attendance.xlsx')
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df.to_excel(excel_file, index=False)
            self.status.setText("[INFO] Exported to Excel.")
        else:
            self.status.setText("[WARNING] No attendance to export.")

    def handle_logout(self):
        QtWidgets.QMessageBox.information(self, "Logout", "You have been logged out.")
        QtWidgets.qApp.exit(MainWindow.EXIT_CODE_REBOOT)

    def handle_go_back(self):
        self.close()
        QtWidgets.qApp.exit(MainWindow.EXIT_CODE_RESTART)

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        if self.timer:
            self.timer.stop()
        event.accept()


# Constants for exit codes to restart the app or go back to login
MainWindow.EXIT_CODE_RESTART = 100
MainWindow.EXIT_CODE_REBOOT = 101
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(student_name="Test User")
    main_window.show()
    sys.exit(app.exec_())