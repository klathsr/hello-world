"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):

    go_to_add = Signal()

    def __init__(self):
        super().__init__()
        self._cards: list[StudentCard] = []
        self.setAcceptDrops(True)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(
            f"color:{C['muted']};font-size:13px;"
        )

        btn_add = QPushButton("+ Add Student")
        btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        btn_add.clicked.connect(self.go_to_add.emit)

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(btn_add)

        # ── empty label ──
        self._lbl_empty = QLabel(
            "No students registered yet.\nClick \"+ Add Student\" to get started."
        )
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._lbl_empty.setStyleSheet(
            f"color:{C['muted']};font-size:13px;"
        )

        # ── scroll area ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(SCROLL_SS)
        self._scroll.setVisible(False)

        self._container = QWidget()
        self._container.setStyleSheet(f"background:{C['bg']};")
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setContentsMargins(32, 20, 32, 20)
        self._card_lay.setSpacing(8)
        self._card_lay.addStretch()

        self._scroll.setWidget(self._container)

        root.addWidget(bar)
        root.addWidget(self._lbl_empty, stretch=1)
        root.addWidget(self._scroll, stretch=1)

    # ── public ───────────────────────────────────────────────
    def add_student(self, data: dict):
        # create card and connect the delete signal
        card = StudentCard(data)
        card.delete_requested.connect(self._remove_card)

        # Add card to the list
        self._cards.append(card)

        # insert card before the trailing stretch
        idx = self._card_lay.count() - 1
        self._card_lay.insertWidget(idx, card)

        self._refresh_count()
        self._refresh_empty()

    # ── private ──────────────────────────────────────────────
    def _remove_card(self, card: StudentCard):
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['fullname']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # remove card from the list
            self._cards.remove(card)
            # remove card from layout
            self._card_lay.removeWidget(card)
            card.deleteLater()
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        n = len(self._cards)
        self.lbl_count.setText(f"{n} enrolled")

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)
        self._scroll.setVisible(has)

    # ── drag-drop reorder ────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target:
            return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)

        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):

    go_back    = Signal()           # Cancel → Page 1
    go_review  = Signal(dict)       # Review → Page 3 with data

    def __init__(self):
        super().__init__()
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── personal info ─────────────────────────────────────
        form.addWidget(section_label("Personal Information"))

        # Student ID
        id_row = QHBoxLayout()
        id_row.addWidget(field_label("Student ID *"))
        self.inp_id = self._inp("e.g. 65010001")
        id_row.addWidget(self.inp_id)
        form.addLayout(id_row)

        # First / Last name
        name_row = QHBoxLayout()
        name_row.setSpacing(16)
        fl = QHBoxLayout()
        fl.addWidget(field_label("First Name *"))
        self.inp_first = self._inp("First name")
        fl.addWidget(self.inp_first)
        ll = QHBoxLayout()
        ll.addWidget(field_label("Last Name *"))
        self.inp_last = self._inp("Last name")
        ll.addWidget(self.inp_last)
        name_row.addLayout(fl, stretch=1)
        name_row.addLayout(ll, stretch=1)
        form.addLayout(name_row)

        # Faculty / Major
        fm_row = QHBoxLayout()
        fm_row.setSpacing(16)
        fac_l = QHBoxLayout()
        fac_l.addWidget(field_label("Faculty *"))
        self.inp_faculty = self._inp("e.g. Science & Technology")
        fac_l.addWidget(self.inp_faculty)
        maj_l = QHBoxLayout()
        maj_l.addWidget(field_label("Major *"))
        self.inp_major = self._inp("e.g. Computer Science")
        maj_l.addWidget(self.inp_major)
        fm_row.addLayout(fac_l, stretch=1)
        fm_row.addLayout(maj_l, stretch=1)
        form.addLayout(fm_row)

        form.addWidget(divider())

        # ── course selection ──────────────────────────────────
        form.addWidget(section_label("Course Selection  (choose 1–3)"))

        self._combos: list[QComboBox] = []
        for i in range(1, 4):
            row = QHBoxLayout()
            row.addWidget(field_label(f"Course {i}"))
            cb = QComboBox()
            cb.addItems(COURSES)
            cb.setMinimumHeight(38)
            cb.setStyleSheet(COMBO_SS)
            self._combos.append(cb)
            row.addWidget(cb)
            form.addLayout(row)

        # ── error label ───────────────────────────────────────
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']};font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        bc = QPushButton("← Cancel")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        bc.clicked.connect(self._on_cancel)

        br = QPushButton("Review →")
        br.setCursor(QCursor(Qt.PointingHandCursor))
        br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        br.clicked.connect(self._on_review)

        btn_row.addWidget(bc)
        btn_row.addStretch()
        btn_row.addWidget(br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)

    def _on_cancel(self):
        self.clear_form()
        self.go_back.emit()

    def _on_review(self):
        # Collect values
        sid      = self.inp_id.text().strip()
        first    = self.inp_first.text().strip()
        last     = self.inp_last.text().strip()
        faculty  = self.inp_faculty.text().strip()
        major    = self.inp_major.text().strip()
        courses  = [
            cb.currentText()
            for cb in self._combos
            if cb.currentIndex() != 0          # index 0 = placeholder
        ]

        # Validate
        missing = []
        if not sid:     missing.append("Student ID")
        if not first:   missing.append("First Name")
        if not last:    missing.append("Last Name")
        if not faculty: missing.append("Faculty")
        if not major:   missing.append("Major")
        if not courses: missing.append("at least 1 course")

        if missing:
            self.lbl_err.setText("Required: " + ",  ".join(missing))
            return

        self.lbl_err.setText("")

        data = {
            "student_id": sid,
            "fullname":   f"{first} {last}",
            "first":      first,
            "last":       last,
            "faculty":    faculty,
            "major":      major,
        }
        for i, cb in enumerate(self._combos, start=1):
            data[f"course{i}"] = cb.currentText() if cb.currentIndex() != 0 else ""

        self.go_review.emit(data)

    def load_data(self, d: dict):
        """Pre-fill form when user clicks Edit on Page 3."""
        self.inp_id.setText(d.get("student_id", ""))
        self.inp_first.setText(d.get("first", ""))
        self.inp_last.setText(d.get("last", ""))
        self.inp_faculty.setText(d.get("faculty", ""))
        self.inp_major.setText(d.get("major", ""))
        for i, cb in enumerate(self._combos, start=1):
            val = d.get(f"course{i}", "")
            idx = cb.findText(val)
            cb.setCurrentIndex(idx if idx >= 0 else 0)
        self.lbl_err.setText("")

    def clear_form(self):
        for w in (self.inp_id, self.inp_first, self.inp_last,
                  self.inp_faculty, self.inp_major):
            w.clear()
        for cb in self._combos:
            cb.setCurrentIndex(0)
        self.lbl_err.setText("")


# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewPage(QWidget):

    confirmed = Signal(dict)   # emit data to Page 1
    go_edit   = Signal(dict)   # emit data back to Page 2

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']};font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── summary section ───────────────────────────────────
        form.addWidget(section_label("Student Information"))

        self._val_id     = self._row(form, "Student ID")
        self._val_name   = self._row(form, "Full Name")
        self._val_fac    = self._row(form, "Faculty")
        self._val_major  = self._row(form, "Major")

        form.addWidget(divider())
        form.addWidget(section_label("Courses"))

        self._val_courses: list[QLabel] = []
        for i in range(1, 4):
            v = self._row(form, f"Course {i}")
            self._val_courses.append(v)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        be = QPushButton("← Edit")
        be.setCursor(QCursor(Qt.PointingHandCursor))
        be.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        be.clicked.connect(lambda: self.go_edit.emit(self._data))

        bc = QPushButton("Confirm Registration")
        bc.setCursor(QCursor(Qt.PointingHandCursor))
        bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        bc.clicked.connect(self._on_confirm)

        btn_row.addWidget(be)
        btn_row.addStretch()
        btn_row.addWidget(bc)
        form.addLayout(btn_row)

        root.addWidget(bar)
        root.addWidget(body, stretch=1)

    def load_data(self, d: dict):
        self._data = d
        self._val_id.setText(d.get("student_id", "—"))
        self._val_name.setText(d.get("fullname", "—"))
        self._val_fac.setText(d.get("faculty", "—"))
        self._val_major.setText(d.get("major", "—"))
        for i, lbl in enumerate(self._val_courses, start=1):
            val = d.get(f"course{i}", "")
            lbl.setText(val if val else "—")

    def _on_confirm(self):
        self.confirmed.emit(self._data)
        QMessageBox.information(
            self, "Success",
            f"Student {self._data.get('fullname', '')} has been registered!"
        )


# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        central = QWidget()
        outer = QVBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        self.setCentralWidget(central)

        # Pages
        self._page1 = StudentListPage()
        self._page2 = AddStudentPage()
        self._page3 = ReviewPage()

        # Stack
        self._stack = QStackedWidget()
        self._stack.addWidget(self._page1)   # index 0
        self._stack.addWidget(self._page2)   # index 1
        self._stack.addWidget(self._page3)   # index 2
        outer.addWidget(self._stack)

        # ── wire signals ──────────────────────────────────────
        # Page 1 → Page 2
        self._page1.go_to_add.connect(lambda: self._stack.setCurrentIndex(1))

        # Page 2 → Page 1 (cancel)
        self._page2.go_back.connect(lambda: self._stack.setCurrentIndex(0))

        # Page 2 → Page 3 (review)
        self._page2.go_review.connect(self._go_to_review)

        # Page 3 → Page 2 (edit)
        self._page3.go_edit.connect(self._go_to_edit)

        # Page 3 → Page 1 (confirm)
        self._page3.confirmed.connect(self._on_confirmed)

    def _go_to_review(self, data: dict):
        self._page3.load_data(data)
        self._stack.setCurrentIndex(2)

    def _go_to_edit(self, data: dict):
        self._page2.load_data(data)
        self._stack.setCurrentIndex(1)

    def _on_confirmed(self, data: dict):
        self._page1.add_student(data)
        self._page2.clear_form()
        self._stack.setCurrentIndex(0)


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
