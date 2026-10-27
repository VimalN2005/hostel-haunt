"""Tests for SQLite database operations in Hostel Haunt."""

import os
import tempfile
import pytest
from hostel_haunt import db


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db.init_db(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_init_and_tables(temp_db):
    conn = db.get_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()

    assert "night_watch" in tables
    assert "exam_haunt" in tables
    assert "memory_vault" in tables
    assert "family_echoes" in tables


def test_night_watch_crud(temp_db):
    entry_id = db.add_night_watch(
        title="Creaking Wardrobe Door",
        location="Room 214",
        sensory_details="Metallic squeak every 15 minutes",
        generated_story="The metal hinges whispered old secrets...",
        spook_rating=8,
        tags="room,night",
        db_path=temp_db,
    )
    assert entry_id > 0

    records = db.get_all_night_watches(temp_db)
    assert len(records) == 1
    assert records[0]["title"] == "Creaking Wardrobe Door"
    assert records[0]["spook_rating"] == 8


def test_exam_haunt_crud(temp_db):
    entry_id = db.add_exam_haunt(
        subject="Algorithms",
        target_score=90.0,
        current_score=50.0,
        hours_slept=4.0,
        backlog_status="moderate",
        spectral_warning="Beware the NP-complete specter!",
        action_plan="Study Dynamic Programming now.",
        db_path=temp_db,
    )
    assert entry_id > 0

    records = db.get_all_exam_haunts(temp_db)
    assert len(records) == 1
    assert records[0]["subject"] == "Algorithms"
    assert records[0]["target_score"] == 90.0


def test_memory_vault_crud(temp_db):
    entry_id = db.add_memory(
        title="Mess Birthday Bash",
        category="Hostel Room Banter",
        raw_notes="Threw cake at Shubham at 12 AM.",
        polished_memoir="A crown of frosting and laughter that defied the cold night.",
        emotion_tags="joy,laughter",
        db_path=temp_db,
    )
    assert entry_id > 0

    records = db.get_all_memories(temp_db)
    assert len(records) == 1
    assert records[0]["title"] == "Mess Birthday Bash"


def test_family_echoes_and_candle_toggle(temp_db):
    entry_id = db.add_family_echo(
        family_member="Dadi",
        relation="Grandmother",
        blessing_or_note="Jeete raho beta, khush raho.",
        candle_lit=1,
        transcription="Jeete raho beta...",
        db_path=temp_db,
    )
    assert entry_id > 0

    records = db.get_all_family_echoes(temp_db)
    assert len(records) == 1
    assert records[0]["candle_lit"] == 1

    # Toggle off
    new_state = db.toggle_candle(entry_id, temp_db)
    assert new_state is False

    records_after = db.get_all_family_echoes(temp_db)
    assert records_after[0]["candle_lit"] == 0

    # Toggle on
    new_state = db.toggle_candle(entry_id, temp_db)
    assert new_state is True
