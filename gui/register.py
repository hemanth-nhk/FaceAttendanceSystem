from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QCheckBox
from utils.auth_db import add_student, student_exists

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.handle_register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def toggle_password_visibility(self, state):
        if state == 2:  # Checked
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Both fields are required.")
            return

        if student_exists(username):
            QMessageBox.warning(self, "Duplicate", "Username already exists.")
            return

        if add_student(username, password):
            QMessageBox.information(self, "Success", "Registration successful.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Registration failed.")
