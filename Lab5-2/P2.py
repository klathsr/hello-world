import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(320, 450)
        self.expression = ""
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # --- Title ---
        title = QLabel("Standard")
        title.setFont(QFont("Arial", 13, QFont.Bold))
        main_layout.addWidget(title)

        # --- Display ---
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 22))
        self.display.setStyleSheet("""
            QLineEdit {
                border: none;
                background: transparent;
                padding: 8px;
                font-size: 28px;
            }
        """)
        main_layout.addWidget(self.display)

        # --- Buttons Grid ---
        grid = QGridLayout()
        grid.setSpacing(6)

        buttons = [
            ["%",   "C+",  "C",   "<-"],
            ["1/x", "x^2", "sqrt(x)", "/"],
            ["7",   "8",   "9",   "*"],
            ["4",   "5",   "6",   "-"],
            ["1",   "2",   "3",   "+"],
            ["+/-", "0",   ".",   "="],
        ]

        for row, row_data in enumerate(buttons):
            for col, text in enumerate(row_data):
                btn = QPushButton(text)
                btn.setFixedHeight(48)
                btn.setFont(QFont("Arial", 11))

                if text == "=":
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #4a90d9;
                            color: white;
                            border-radius: 6px;
                            font-weight: bold;
                        }
                        QPushButton:hover { background-color: #357abd; }
                    """)
                elif text in ["C", "C+", "<-", "%"]:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #e0e0e0;
                            color: black;
                            font-weight: bold;
                            border-radius: 6px;
                        }
                        QPushButton:hover { background-color: #c8c8c8; }
                    """)
                elif text in ["+", "-", "*", "/"]:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f0a500;
                            color: black;
                            border-radius: 6px;
                            font-weight: bold;
                        }
                        QPushButton:hover { background-color: #d4940a; }
                    """)
                else:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f5f5f5;
                            color: black;
                            font-weight: bold;
                            border-radius: 6px;
                        }
                        QPushButton:hover { background-color: #e0e0e0; }
                    """)

                btn.clicked.connect(lambda checked, t=text: self.on_button_click(t))
                grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def on_button_click(self, text):
        if text == "C":
            self.expression = ""
            self.display.setText("")

        elif text == "C+":
            pass

        elif text == "<-":
            self.expression = self.expression[:-1]
            self.display.setText(self.expression)

        elif text == "=":
            try:
                result = eval(self.expression)
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        elif text == "%":
            try:
                result = eval(self.expression) / 100
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        elif text == "1/x":
            try:
                result = 1 / eval(self.expression)
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        elif text == "x^2":
            try:
                result = eval(self.expression) ** 2
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        elif text == "sqrt(x)":
            try:
                result = math.sqrt(eval(self.expression))
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        elif text == "+/-":
            try:
                result = eval(self.expression) * -1
                self.display.setText(str(result))
                self.expression = str(result)
            except:
                self.display.setText("Error")
                self.expression = ""

        else:
            self.expression += text
            self.display.setText(self.expression)


def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()