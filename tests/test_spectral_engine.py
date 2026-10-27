"""Tests for the Spectral Intelligence Engine."""

import pytest
from unittest.mock import patch
from hostel_haunt.spectral_engine import SpectralEngine


def test_procedural_fallback_night_tale():
    engine = SpectralEngine(host="http://non-existent-host:9999")
    story = engine.weave_night_tale(
        title="Midnight Corridor Whispers",
        location="Wing 4",
        sensory_details="Cold draft and flickering bulb",
        spook_level=8,
    )
    assert len(story) > 50
    assert "Wing 4" in story or "midnight" in story.lower() or "cold draft" in story.lower() or "bulb" in story.lower()


def test_procedural_fallback_exam_prophecy():
    engine = SpectralEngine(host="http://non-existent-host:9999")
    res = engine.summon_exam_prophecy(
        subject="Database Systems",
        target_score=80.0,
        current_score=40.0,
        hours_slept=2.0,
        backlog_status="high",
    )
    assert "warning" in res
    assert "action_plan" in res
    assert "Database Systems" in res["warning"]
    assert "2004" in res["warning"]


def test_procedural_fallback_crystallize_memory():
    engine = SpectralEngine(host="http://non-existent-host:9999")
    memoir = engine.crystallize_memory(
        title="Night Walk by the Lake",
        category="Campus Walks",
        raw_notes="Talked about life and future startups until 4 AM.",
        emotion_tags="nostalgia,ambition",
    )
    assert "NIGHT WALK BY THE LAKE" in memoir
    assert "Campus Walks" in memoir
    assert "Talked about life" in memoir


def test_procedural_fallback_honor_family_voice():
    engine = SpectralEngine(host="http://non-existent-host:9999")
    blessing = engine.honor_family_voice(
        member="Papa",
        relation="Father",
        note_or_blessing="Mehnat karte raho, parinaam ki chinta mat karo.",
    )
    assert "Papa" in blessing
    assert "Father" in blessing
    assert "Mehnat karte raho" in blessing


def test_ollama_mocked_success():
    engine = SpectralEngine()
    with patch.object(engine, "_call_ollama", return_value="The spirit of Gemma whispers from the terminal..."):
        tale = engine.weave_night_tale("Spooky Event", "Mess", "Plates clinking", 9)
        assert tale == "The spirit of Gemma whispers from the terminal..."
