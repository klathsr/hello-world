from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C


class StudentCard(QFrame):

    # Signal for delete request: emits self
    delete_requested = Signal(object)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data

        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))

        self._build()

    def _build(self):
        # Collect non-empty courses
        courses = [
            self.data.get(f"course{i}", "")
            for i in range(1, 4)
            if self.data.get(f"course{i}", "") and self.data.get(f"course{i}", "") != "— Select Course —"
        ]

        # base height: name + dept rows, plus 20px per course line
        self.setMinimumHeight(70 + len(courses) * 20)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
                border-radius:8px;
                margin:2px 0px;
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(8)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(
            f"background:transparent; color:{C['muted']};font-size:18px;padding-top:2px;"
        )

        # content area
        content = QVBoxLayout()
        content.setSpacing(2)

        # Name + ID row
        name_row = QHBoxLayout()
        name_row.setSpacing(8)

        name_lbl = QLabel(self.data.get("fullname", ""))
        name_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        name_lbl.setStyleSheet(f"background:transparent; color:{C['text']};")

        id_lbl = QLabel(self.data.get("student_id", ""))
        id_lbl.setStyleSheet(f"background:transparent; color:{C['muted']};font-size:11px;")

        name_row.addWidget(name_lbl)
        name_row.addWidget(id_lbl)
        name_row.addStretch()

        # Faculty / Major row
        dept_lbl = QLabel(
            f"{self.data.get('faculty', '')}  ·  {self.data.get('major', '')}"
        )
        dept_lbl.setStyleSheet(f"background:transparent; color:{C['muted']};font-size:11px;")

        content.addLayout(name_row)
        content.addWidget(dept_lbl)

        # Course rows
        for course in courses:
            c_lbl = QLabel(course)
            c_lbl.setStyleSheet(
                f"background:transparent; color:{C['text']};font-size:11px;"
            )
            content.addWidget(c_lbl)

        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:11px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}
        """)
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))

        outer.addWidget(handle, alignment=Qt.AlignTop)
        outer.addLayout(content, stretch=1)
        outer.addWidget(btn_del, alignment=Qt.AlignTop)

    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)
