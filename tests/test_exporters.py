"""Tests for Markdown and JSON Exporters."""

import os
import json
import tempfile
from hostel_haunt import db
from hostel_haunt.exporters import export_markdown_chronicle, export_json_backup


def test_export_markdown_and_json():
    fd, temp_db = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db.init_db(temp_db)

    db.add_night_watch("Echo in Corridor", "Wing 1", "Tap dripping", "Spooky tale here", db_path=temp_db)
    db.add_exam_haunt("Maths", 100, 50, 4, "ok", "Warning", "Plan", db_path=temp_db)
    db.add_memory("Chai", "Hostel Banter", "Raw notes", "Polished memoir", db_path=temp_db)
    db.add_family_echo("Maa", "Mother", "Blessing", db_path=temp_db)

    temp_out_md = tempfile.mktemp(suffix=".md")
    md_file = export_markdown_chronicle(output_path=temp_out_md, db_path=temp_db)
    assert os.path.exists(md_file)
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
    assert "HOSTEL HAUNT: THE SPECTRAL CHRONICLE" in md_text
    assert "Echo in Corridor" in md_text
    assert "Maths" in md_text
    assert "Chai" in md_text
    assert "Maa" in md_text

    temp_out_json = tempfile.mktemp(suffix=".json")
    json_file = export_json_backup(output_path=temp_out_json, db_path=temp_db)
    assert os.path.exists(json_file)
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["metadata"]["app"] == "Hostel Haunt"
    assert len(data["night_watch"]) == 1
    assert len(data["exam_haunt"]) == 1
    assert len(data["memory_vault"]) == 1
    assert len(data["family_echoes"]) == 1

    # Cleanup
    if os.path.exists(temp_db):
        os.remove(temp_db)
    if os.path.exists(temp_out_md):
        os.remove(temp_out_md)
    if os.path.exists(temp_out_json):
        os.remove(temp_out_json)
