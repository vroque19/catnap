import sqlite3
import os
from datetime import datetime

DATABASE_PATH = "instance/sleeptracker.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = get_db_connection()
    c = conn.cursor()
    # Create settings table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            bed_time TEXT NOT NULL,
            wake_time TEXT NOT NULL
        )
    """
    )

    # Create sleep data table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            light INTEGER NOT NULL,
            temperature REAL NOT NULL,
            motion BOOLEAN NOT NULL
        )
    """
    )

    c.execute(
        """
            CREATE TABLE IF NOT EXISTS sleep_scores (
            if INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            day TEXT NOT NULL,
            score INTEGER NOT NULL
            )
        """
    )
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS sensor_data_archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            date TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            light INTEGER NOT NULL,
            temperature REAL NOT NULL,
            motion BOOLEAN NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
init_db()
