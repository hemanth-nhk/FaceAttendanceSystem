import os
import csv
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class ProfileDialog(QDialog):
    def __init__(self, student_name):
        super().__init__()
        self.setWindowTitle("Student Profile")
        self.resize(300, 200)

        layout = QVBoxLayout()

        name_label = QLabel(f"<b>Name:</b> {student_name}")
        layout.addWidget(name_label)

        attendance_file = os.path.join(os.path.dirname(__file__), '..', 'attendance.csv')
        count = 0
        last_time = "N/A"

        if os.path.exists(attendance_file):
            with open(attendance_file, 'r') as f:
                rows = list(csv.reader(f))[1:]  # Skip header
                student_rows = [row for row in rows if row[0] == student_name]
                count = len(student_rows)
                if count > 0:
                    last_time = student_rows[-1][1]

        count_label = QLabel(f"<b>Total Attendances:</b> {count}")
        layout.addWidget(count_label)

        last_label = QLabel(f"<b>Last Attendance:</b> {last_time}")
        layout.addWidget(last_label)

        self.setLayout(layout)
        self.setStyleSheet("QDialog { background-color: #f0f0f0; } QLabel { font-size: 14px; }")    