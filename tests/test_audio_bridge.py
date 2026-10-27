"""Tests for Audio Bridge and Voice Notes."""

import os
import tempfile
from pathlib import Path
from hostel_haunt.audio_bridge import AudioBridge


def test_audio_bridge_save_bytes():
    temp_dir = Path(tempfile.mkdtemp())
    bridge = AudioBridge(storage_dir=temp_dir)

    dummy_bytes = b"RIFF....WAVEfmt ...."
    saved_path = bridge.save_audio_file(dummy_bytes, "test_voice.wav")

    assert os.path.exists(saved_path)
    assert Path(saved_path).name == "test_voice.wav"
    assert os.path.getsize(saved_path) == len(dummy_bytes)


def test_audio_bridge_transcribe_fallback():
    temp_dir = Path(tempfile.mkdtemp())
    bridge = AudioBridge(storage_dir=temp_dir)

    dummy_path = temp_dir / "sample.wav"
    with open(dummy_path, "wb") as f:
        f.write(b"sample audio")

    res = bridge.transcribe(str(dummy_path), simulated_hint="Beta time pe so jao")
    assert res["status"] == "success"
    assert res["text"] == "Beta time pe so jao"
