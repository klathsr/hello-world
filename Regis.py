import sys
from PySide6.QtWidgets import (
    QApplication, QWidget,
    QLabel, QLineEdit, QTextEdit,
    QRadioButton, QButtonGroup,
    QComboBox, QDateEdit,
    QCheckBox, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QMainWindow
)
from PySide6.QtCore import QDate, Qt, QLocale
from PySide6.QtGui import QFont


class StudentRegistrationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("P2: Student Registration")
        self.setFixedSize(400, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        central_widget.setLayout(main_layout)

        # Title
        title = QLabel("Student Registration Form")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(title)
        main_layout.addSpacing(20)

        # Full Name
        main_layout.addWidget(QLabel("Full Name:"))
        self.name_input = QLineEdit()
        main_layout.addWidget(self.name_input)
        main_layout.addSpacing(10)

        # Email
        main_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        main_layout.addWidget(self.email_input)
        main_layout.addSpacing(10)

        # Phone
        main_layout.addWidget(QLabel("Phone:"))
        self.phone_input = QLineEdit()
        main_layout.addWidget(self.phone_input)
        main_layout.addSpacing(15)

        # Date of Birth
        main_layout.addWidget(QLabel("Date of Birth (dd/MM/yyyy):"))
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("dd/MM/yyyy")
        self.dob_input.setDate(QDate(2000, 1, 1))
        self.dob_input.setFixedWidth(150)
        main_layout.addWidget(self.dob_input)
        main_layout.addSpacing(20)

        # Gender
        main_layout.addWidget(QLabel("Gender:"))
        gender_layout = QHBoxLayout()
        self.gender_group = QButtonGroup(self)

        self.male = QRadioButton("Male")
        self.female = QRadioButton("Female")
        self.non_binary = QRadioButton("Non-binary")
        self.prefer_not = QRadioButton("Prefer not to say")

        for btn in [self.male, self.female, self.non_binary, self.prefer_not]:
            self.gender_group.addButton(btn)
            gender_layout.addWidget(btn)

        main_layout.addLayout(gender_layout)
        main_layout.addSpacing(20)

        # Program
        main_layout.addWidget(QLabel("Program:"))
        self.program_combo = QComboBox()
        self.program_combo.addItem("Select your program")
        self.program_combo.addItems([
            "Chemical Engineering"
            "Computer Engineering",
            "Digital Media Engineering",
            "Environmental Engineering",
            "Electrical Engineering",
            "Semiconductor Engineering",
            "Mechanical Engineering",
            "Industrial Engineering",
            "Logistic Engineering",
            "Electronic Engineering",
            "Telecommunication Engineering",
            "Agricultural Engineering",
            "Civil Engineering",
            "ARIS"
        ])
        main_layout.addWidget(self.program_combo)
        main_layout.addSpacing(10)

        # About
        main_layout.addWidget(QLabel("Tell us a little bit about yourself:"))
        self.about_input = QTextEdit()
        self.about_input.setMaximumHeight(100)
        main_layout.addWidget(self.about_input)
        main_layout.addSpacing(15)

        # Terms
        self.terms_checkbox = QCheckBox("I accept the terms and conditions.")
        main_layout.addWidget(self.terms_checkbox)

        main_layout.addStretch()

        # Submit Button
        self.submit_btn = QPushButton("Submit Registration")
        self.submit_btn.setFixedHeight(35)
        main_layout.addWidget(self.submit_btn)


if __name__ == "__main__":
    QLocale.setDefault(QLocale(QLocale.English))
    app = QApplication(sys.argv)
    window = StudentRegistrationForm()
    window.show()
    sys.exit(app.exec())
