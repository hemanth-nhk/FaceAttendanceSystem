import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from gui.register import RegisterDialog
from gui.login import StudentLoginDialog
from gui.interface import MainWindow
from utils.auth_db import init_student_db

def launch_main(name):
    window = MainWindow(student_name=name)
    window.show()
    return window

if __name__ == "__main__":
    init_student_db()
    app = QApplication(sys.argv)

    # Ask user whether to login or register
    choice = QMessageBox.question(
        None,
        "Login or Register",
        "Do you want to Login (Yes) or Register (No)?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.Yes
    )

    student_name = None

    if choice == QMessageBox.No:  # Register
        register_dialog = RegisterDialog()

        # Auto-fill for testing (optional)
        register_dialog.username_input.setText("admin")
        register_dialog.password_input.setText("admin123")

        if register_dialog.exec_() == RegisterDialog.Accepted:
            student_name = register_dialog.username_input.text().strip()
    else:  # Login
        login_dialog = StudentLoginDialog()

        # Auto-fill for testing (optional)
        login_dialog.username_input.setText("admin")
        login_dialog.password_input.setText("admin123")

        if login_dialog.exec_() == StudentLoginDialog.Accepted and login_dialog.authenticated:
            student_name = login_dialog.student_name

    if student_name:
        main_window = launch_main(student_name)
        sys.exit(app.exec_())
    else:
        print("❌ User canceled login or registration. Exiting.")
        sys.exit(0)
