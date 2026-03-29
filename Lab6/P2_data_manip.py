import json
import pandas as pd
import pyqtgraph as pg
import numpy as np

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    TODO 1 — Read a CSV file and return a clean DataFrame.
    """
    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The CSV file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    return df


def read_json(path: str) -> pd.DataFrame:
    """
    TODO 2 — Read a JSON file and return a DataFrame.
    """
    df = pd.read_json(path)

    if df.empty:
        raise ValueError("The JSON file is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"JSON is missing required columns: {missing}")

    return df


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    TODO 3 — Save a DataFrame to a CSV file.
    """
    if df.empty:
        raise ValueError("DataFrame is empty — nothing to save.")

    try:
        df.to_csv(path, index=False)
    except Exception as e:
        raise IOError(f"Failed to write CSV: {e}")


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    TODO 4 — Save a DataFrame to a JSON file.
    """
    if df.empty:
        raise ValueError("DataFrame is empty — nothing to save.")

    try:
        df.to_json(path, orient="records", indent=2)
    except Exception as e:
        raise IOError(f"Failed to write JSON: {e}")


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    TODO 5 — Compute summary statistics per city and return a QTableWidget.
    """
    if df.empty:
        raise ValueError("DataFrame is empty.")

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")

    # ── compute stats per city ────────────────────────────────────────────
    rows_data = []
    for city in CITIES:
        city_df = df[df["city"] == city]
        if city_df.empty:
            continue
        rows_data.append({
            "city":         city,
            "records":      len(city_df),
            "avg_temp":     round(city_df["temp_c"].mean(), 1),
            "hottest":      round(city_df["temp_c"].max(), 1),
            "coldest":      round(city_df["temp_c"].min(), 1),
            "total_rain":   round(city_df["rainfall_mm"].sum(), 1),
            "avg_humidity": round(city_df["humidity"].mean(), 1),
        })

    # ── build QTableWidget ────────────────────────────────────────────────
    headers = [
        "City", "Records", "Avg Temp (°C)",
        "Hottest (°C)", "Coldest (°C)",
        "Total Rain (mm)", "Avg Humidity (%)",
    ]
    table = QTableWidget(len(rows_data), len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setFont(QFont("Segoe UI", 10))

    city_colors = {
        "Bangkok":   QColor(255, 220, 180),
        "Chiang Mai": QColor(180, 220, 255),
        "Phuket":    QColor(180, 255, 200),
    }

    for ri, r in enumerate(rows_data):
        values = [
            r["city"], str(r["records"]),
            str(r["avg_temp"]), str(r["hottest"]), str(r["coldest"]),
            str(r["total_rain"]), str(r["avg_humidity"]),
        ]
        bg = city_colors.get(r["city"], QColor(255, 255, 255))
        for ci, val in enumerate(values):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(bg)
            table.setItem(ri, ci, item)

    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    TODO 6 — Draw a Rainfall Histogram using pyqtgraph and return a PlotWidget.
    """
    if df.empty:
        raise ValueError("DataFrame is empty — no data to chart.")

    if "rainfall_mm" not in df.columns:
        raise ValueError("Column 'rainfall_mm' not found in DataFrame.")

    # ── compute histogram ─────────────────────────────────────────────────
    rainfall = df["rainfall_mm"].dropna().values
    counts, bin_edges = np.histogram(rainfall, bins=15)

    # ── build PlotWidget ──────────────────────────────────────────────────
    pw = pg.PlotWidget()
    pw.setBackground("w")
    pw.setTitle("Rainfall Distribution", color="#333333", size="13pt")
    pw.setLabel("left",   "Frequency",     color="#333333", size="11pt")
    pw.setLabel("bottom", "Rainfall (mm)", color="#333333", size="11pt")
    pw.showGrid(x=True, y=True, alpha=0.3)

    # Draw bars manually using BarGraphItem
    bar_width = bin_edges[1] - bin_edges[0]
    bar_x     = bin_edges[:-1]                  # left edge of each bin

    bars = pg.BarGraphItem(
        x=bar_x, height=counts, width=bar_width * 0.9,
        brush=pg.mkBrush(color=(70, 130, 200, 180)),
        pen=pg.mkPen(color=(40, 80, 150), width=1),
    )
    pw.addItem(bars)

    return pw
