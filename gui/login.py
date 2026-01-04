from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QCheckBox
from utils.auth_db import validate_student

class StudentLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Login")
        self.authenticated = False
        self.student_name = ""

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def toggle_password_visibility(self, state):
        if state == 2:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Both fields are required.")
            return

        if validate_student(username, password):
            self.authenticated = True
            self.student_name = username
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
