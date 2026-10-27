"""SQLite database management for Hostel Haunt.

Provides persistent local storage for all 4 spectral dimensions:
1. Night Watch (Strange nocturnal hostel events -> Ghost lore)
2. Exam Haunt (Academic records & backlogs -> Spectral warnings)
3. Memory Vault (College days & wing camaraderie -> Día de los Muertos memoirs)
4. Family Echoes (Voice notes & home calls -> Sacred remembrance altars)
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from hostel_haunt.config import DB_PATH


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a sqlite3 connection with dict-like row factory."""
    path = db_path or DB_PATH
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Initializes tables for all 4 dimensions if they do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Night Watch: Hostel events -> Ghost stories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS night_watch (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        title TEXT NOT NULL,
        location TEXT NOT NULL,
        sensory_details TEXT NOT NULL,
        generated_story TEXT NOT NULL,
        spook_rating INTEGER DEFAULT 5,
        tags TEXT DEFAULT 'hostel,night'
    );
    """)

    # 2. Exam Haunt: Study logs + past marks -> Motivation + dark warnings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exam_haunt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        subject TEXT NOT NULL,
        target_score REAL,
        current_score REAL,
        hours_slept REAL,
        backlog_status TEXT DEFAULT 'none',
        spectral_warning TEXT NOT NULL,
        action_plan TEXT NOT NULL
    );
    """)

    # 3. Memory Vault: College moments + wing stories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_vault (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        raw_notes TEXT NOT NULL,
        polished_memoir TEXT NOT NULL,
        emotion_tags TEXT DEFAULT 'nostalgia',
        candle_color TEXT DEFAULT '#ff9900'
    );
    """)

    # 4. Family Echoes: Family voice notes -> Remembrance & Día de los Muertos spirit
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS family_echoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        family_member TEXT NOT NULL,
        relation TEXT NOT NULL,
        blessing_or_note TEXT NOT NULL,
        audio_path TEXT DEFAULT '',
        candle_lit INTEGER DEFAULT 1,
        transcription TEXT DEFAULT ''
    );
    """)

    conn.commit()
    conn.close()


# --- CRUD Helpers: Night Watch ---

def add_night_watch(
    title: str,
    location: str,
    sensory_details: str,
    generated_story: str,
    spook_rating: int = 5,
    tags: str = "hostel,night",
    db_path: Optional[str] = None,
) -> int:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO night_watch (timestamp, title, location, sensory_details, generated_story, spook_rating, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (now, title, location, sensory_details, generated_story, spook_rating, tags),
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id


def get_all_night_watches(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM night_watch ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# --- CRUD Helpers: Exam Haunt ---

def add_exam_haunt(
    subject: str,
    target_score: float,
    current_score: float,
    hours_slept: float,
    backlog_status: str,
    spectral_warning: str,
    action_plan: str,
    db_path: Optional[str] = None,
) -> int:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO exam_haunt (timestamp, subject, target_score, current_score, hours_slept, backlog_status, spectral_warning, action_plan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (now, subject, target_score, current_score, hours_slept, backlog_status, spectral_warning, action_plan),
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id


def get_all_exam_haunts(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exam_haunt ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# --- CRUD Helpers: Memory Vault ---

def add_memory(
    title: str,
    category: str,
    raw_notes: str,
    polished_memoir: str,
    emotion_tags: str = "nostalgia",
    candle_color: str = "#ff9900",
    db_path: Optional[str] = None,
) -> int:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO memory_vault (timestamp, title, category, raw_notes, polished_memoir, emotion_tags, candle_color)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (now, title, category, raw_notes, polished_memoir, emotion_tags, candle_color),
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id


def get_all_memories(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory_vault ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# --- CRUD Helpers: Family Echoes ---

def add_family_echo(
    family_member: str,
    relation: str,
    blessing_or_note: str,
    audio_path: str = "",
    candle_lit: int = 1,
    transcription: str = "",
    db_path: Optional[str] = None,
) -> int:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO family_echoes (timestamp, family_member, relation, blessing_or_note, audio_path, candle_lit, transcription)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (now, family_member, relation, blessing_or_note, audio_path, candle_lit, transcription),
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id


def get_all_family_echoes(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM family_echoes ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def toggle_candle(echo_id: int, db_path: Optional[str] = None) -> bool:
    """Toggles the candle lit state on an ofrenda family echo."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT candle_lit FROM family_echoes WHERE id = ?", (echo_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    new_state = 0 if row["candle_lit"] == 1 else 1
    cursor.execute("UPDATE family_echoes SET candle_lit = ? WHERE id = ?", (new_state, echo_id))
    conn.commit()
    conn.close()
    return bool(new_state)
