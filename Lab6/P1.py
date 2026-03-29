import sys
import json
from datetime import date
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QDialog, QLineEdit,
    QCalendarWidget, QComboBox, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QDate, QLocale
from PySide6.QtGui import QFont


# ──────────────────────────────────────────────
# Task Card Widget
# ──────────────────────────────────────────────
PRIORITY_COLORS = {
    "Low":      "#d4edda",   # soft green
    "Medium":   "#cce5ff",   # soft blue
    "High":     "#fff3cd",   # soft yellow
    "Critical": "#f8d7da",   # soft red
}

PRIORITY_BADGE_COLORS = {
    "Low":      "#28a745",
    "Medium":   "#007bff",
    "High":     "#ffc107",
    "Critical": "#dc3545",
}


class TaskCard(QFrame):
    def __init__(self, task: dict, on_done_callback):
        super().__init__()
        self.task = task
        self.on_done_callback = on_done_callback
        self._build_ui()

    def _build_ui(self):
        priority = self.task.get("priority", "Low")
        bg = PRIORITY_COLORS.get(priority, "#ffffff")
        badge_bg = PRIORITY_BADGE_COLORS.get(priority, "#6c757d")

        self.setStyleSheet(f"""
            TaskCard {{
                background-color: {bg};
                border-radius: 8px;
                border: 1px solid rgba(0,0,0,0.1);
            }}
        """)
        self.setFixedHeight(90)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(12, 8, 12, 8)

        # Left: title + deadline
        left = QVBoxLayout()
        left.setSpacing(4)

        title_lbl = QLabel(self.task.get("title", ""))
        title_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title_lbl.setStyleSheet("background: transparent; border: none;")

        deadline_lbl = QLabel(f"📅 {self.task.get('deadline', '')}")
        deadline_lbl.setStyleSheet("background: transparent; border: none; color: #555;")

        left.addWidget(title_lbl)
        left.addWidget(deadline_lbl)
        left.addStretch()

        # Right: priority badge + done button
        right = QVBoxLayout()
        right.setSpacing(4)
        right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        done_btn = QPushButton("✓ Done")
        done_btn.setFixedSize(80, 26)
        done_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d; color: white;
                border-radius: 4px; font-size: 11px;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        done_btn.clicked.connect(self._mark_done)

        badge = QLabel(priority)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setFixedSize(70, 22)
        badge.setStyleSheet(f"""
            background-color: {badge_bg}; color: white;
            border-radius: 4px; font-size: 10px; font-weight: bold;
            border: none;
        """)

        right.addWidget(done_btn)
        right.addWidget(badge, 0, Qt.AlignmentFlag.AlignRight)

        outer.addLayout(left, stretch=1)
        outer.addLayout(right)

    def _mark_done(self):
        self.task["done"] = True
        self.on_done_callback(self)


# ──────────────────────────────────────────────
# Add Task Dialog
# ──────────────────────────────────────────────
class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setMinimumWidth(380)
        self.result_task = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(16, 16, 16, 16)

        layout.addWidget(QLabel("New Task"))

        # Task name
        name_row = QHBoxLayout()
        name_lbl = QLabel("Task:")
        name_lbl.setFixedWidth(70)
        name_row.addWidget(name_lbl)
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter task name...")
        name_row.addWidget(self.task_input)
        layout.addLayout(name_row)

        # Priority
        prio_row = QHBoxLayout()
        prio_lbl = QLabel("Priority:")
        prio_lbl.setFixedWidth(70)
        prio_row.addWidget(prio_lbl)
        self.priority_box = QComboBox()
        self.priority_box.addItems(["Low", "Medium", "High", "Critical"])
        prio_row.addWidget(self.priority_box)
        layout.addLayout(prio_row)

        # Deadline row with toggle
        deadline_row = QHBoxLayout()
        deadline_lbl = QLabel("Deadline:")
        deadline_lbl.setFixedWidth(70)
        deadline_row.addWidget(deadline_lbl)
        self.date_display = QPushButton(QDate.currentDate().toString("dd-MM-yyyy"))
        self.date_display.setStyleSheet("""
            QPushButton {
                background-color: white; border: 1px solid #ccc;
                border-radius: 4px; padding: 4px 8px; text-align: left;
            }
            QPushButton:hover { border-color: #007bff; }
        """)
        self.date_display.clicked.connect(self._toggle_calendar)
        deadline_row.addWidget(self.date_display)
        layout.addLayout(deadline_row)

        # Calendar — hidden by default
        self.calendar = QCalendarWidget()
        self.calendar.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates))
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.setGridVisible(True)
        self.calendar.setFixedSize(340, 220)
        self.calendar.clicked.connect(self._on_date_selected)
        self.calendar.setVisible(False)
        layout.addWidget(self.calendar)

        # Buttons
        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(34)
        cancel_btn.clicked.connect(self.reject)
        add_btn = QPushButton("Add Task")
        add_btn.setFixedHeight(34)
        add_btn.setStyleSheet("background-color: #007bff; color: white; border-radius: 4px; padding: 6px;")
        add_btn.clicked.connect(self._add_task)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(add_btn)
        layout.addLayout(btn_row)

    def _toggle_calendar(self):
        visible = not self.calendar.isVisible()
        self.calendar.setVisible(visible)
        self.adjustSize()

    def _on_date_selected(self, qdate):
        self.date_display.setText(qdate.toString("dd-MM-yyyy"))
        self.calendar.setVisible(False)
        self.adjustSize()

    def _add_task(self):
        title = self.task_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing Title", "Please enter a task name.")
            return
        # Convert display format dd-MM-yyyy → yyyy-MM-dd for JSON
        display_date = self.date_display.text()
        qdate = QDate.fromString(display_date, "dd-MM-yyyy")
        deadline = qdate.toString("yyyy-MM-dd")
        priority = self.priority_box.currentText()
        self.result_task = {
            "title": title,
            "deadline": deadline,
            "priority": priority,
            "done": False
        }
        self.accept()


# ──────────────────────────────────────────────
# Main Window
# ──────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My To-Do List")
        self.setMinimumSize(520, 560)
        self.tasks: list[dict] = []
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # Header
        header = QHBoxLayout()
        title = QLabel("My To-Do List")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.count_lbl = QLabel("0 tasks")
        self.count_lbl.setStyleSheet("color: #888;")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.count_lbl)
        root.addLayout(header)

        # Toolbar
        toolbar = QHBoxLayout()
        add_btn = QPushButton("+ Add Task")
        add_btn.setStyleSheet("background-color: #007bff; color: white; border-radius: 4px; padding: 6px 12px;")
        add_btn.clicked.connect(self._open_add_dialog)

        load_btn = QPushButton("📂 Load JSON")
        load_btn.setStyleSheet("background-color: #28a745; color: white; border-radius: 4px; padding: 6px 12px;")
        load_btn.clicked.connect(self._load_json)

        save_btn = QPushButton("💾 Save JSON")
        save_btn.setStyleSheet("background-color: #17a2b8; color: white; border-radius: 4px; padding: 6px 12px;")
        save_btn.clicked.connect(self._save_json)

        toolbar.addWidget(add_btn)
        toolbar.addWidget(load_btn)
        toolbar.addWidget(save_btn)
        toolbar.addStretch()
        root.addLayout(toolbar)

        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cards_layout.setSpacing(8)

        scroll.setWidget(self.cards_container)
        root.addWidget(scroll)

        self._refresh_empty_label()

    def _refresh_empty_label(self):
        done_count = sum(1 for t in self.tasks if t.get("done"))
        active_count = len(self.tasks) - done_count
        self.count_lbl.setText(f"{done_count}/{len(self.tasks)} done")

        # Check if any non-done cards are visible
        if active_count == 0:
            if not hasattr(self, '_empty_lbl') or self._empty_lbl is None:
                self._empty_lbl = QLabel("No tasks yet.\nClick + Add Task to get started!")
                self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._empty_lbl.setStyleSheet("color: #aaa; font-size: 14px;")
                self.cards_layout.addWidget(self._empty_lbl)
            try:
                self._empty_lbl.setVisible(True)
            except RuntimeError:
                self._empty_lbl = QLabel("No tasks yet.\nClick + Add Task to get started!")
                self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._empty_lbl.setStyleSheet("color: #aaa; font-size: 14px;")
                self.cards_layout.addWidget(self._empty_lbl)
        else:
            if hasattr(self, '_empty_lbl') and self._empty_lbl is not None:
                try:
                    self._empty_lbl.setVisible(False)
                except RuntimeError:
                    pass
                self._empty_lbl = None

    def _render_tasks(self):
        # Clear existing cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Render only not-done tasks
        for task in self.tasks:
            if not task.get("done"):
                card = TaskCard(task, self._on_card_done)
                self.cards_layout.addWidget(card)

        self._refresh_empty_label()

    def _on_card_done(self, card: TaskCard):
        # Mark done in data, remove card from view
        card.setVisible(False)
        self.cards_layout.removeWidget(card)
        card.deleteLater()
        self._refresh_empty_label()

    def _open_add_dialog(self):
        dlg = AddTaskDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.result_task:
            self.tasks.append(dlg.result_task)
            card = TaskCard(dlg.result_task, self._on_card_done)
            self.cards_layout.addWidget(card)
            self._refresh_empty_label()

    def _load_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Tasks", "", "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if not isinstance(loaded, list):
                raise ValueError("Expected a JSON array.")
            self.tasks = loaded
            self._render_tasks()
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    def _save_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Tasks", "tasks.json", "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Saved", f"Tasks saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())