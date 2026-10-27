"""Export utilities for Hostel Haunt.

Generates beautiful Markdown, HTML ofrenda books, and JSON archives
of all memories, night chronicles, exam survival directives, and family blessings.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from hostel_haunt.config import EXPORTS_DIR
from hostel_haunt.db import (
    get_all_night_watches,
    get_all_exam_haunts,
    get_all_memories,
    get_all_family_echoes,
)


def export_markdown_chronicle(output_path: Optional[str] = None, db_path: Optional[str] = None) -> str:
    """Generates a complete Markdown chronicle book of the hostel haunting."""
    night_watches = get_all_night_watches(db_path)
    exam_haunts = get_all_exam_haunts(db_path)
    memories = get_all_memories(db_path)
    echoes = get_all_family_echoes(db_path)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = [
        f"# 🕯️ HOSTEL HAUNT: THE SPECTRAL CHRONICLE",
        f"*Preserved on {timestamp} by Hostel Haunt AI*",
        f"\n> *\"The ghost that lives in your laptop and remembers what the night, the exams, the family calls, and the empty corridors try to forget.\"*\n",
        "---\n",
        "## 🌙 Section I: Night Watch Chronicles\n",
    ]

    if not night_watches:
        md.append("_No nocturnal events recorded yet._\n")
    else:
        for item in night_watches:
            md.append(f"### 👻 {item['title']} ({item['location']})")
            md.append(f"**Recorded:** {item['timestamp']} | **Spook Rating:** {item['spook_rating']}/10")
            md.append(f"\n{item['generated_story']}\n")

    md.append("\n---\n## 📚 Section II: Exam Haunt & Academic Prophecies\n")
    if not exam_haunts:
        md.append("_No exam haunts summoned yet._\n")
    else:
        for item in exam_haunts:
            md.append(f"### ⚠️ Subject: {item['subject']}")
            md.append(f"**Target:** {item['target_score']} | **Score:** {item['current_score']} | **Sleep:** {item['hours_slept']} hrs")
            md.append(f"\n{item['spectral_warning']}\n")
            md.append(f"\n**Directive:**\n{item['action_plan']}\n")

    md.append("\n---\n## 🌼 Section III: Memory Vault (Día de los Muertos Altar)\n")
    if not memories:
        md.append("_The memory vault is silent._\n")
    else:
        for item in memories:
            md.append(f"### 🕯️ {item['title']} [{item['category']}]")
            md.append(f"**Emotions:** {item['emotion_tags']} | **Date:** {item['timestamp']}")
            md.append(f"\n{item['polished_memoir']}\n")

    md.append("\n---\n## 🧡 Section IV: Family Echoes (The Ancestral Hearth)\n")
    if not echoes:
        md.append("_No family echoes placed on the altar._\n")
    else:
        for item in echoes:
            candle_icon = "🔥 Candle Lit" if item["candle_lit"] else "🕯️ Extinguished"
            md.append(f"### 🌼 {item['family_member']} ({item['relation']}) — {candle_icon}")
            md.append(f"**Blessing / Note:** \"{item['blessing_or_note']}\"")
            if item.get("transcription"):
                md.append(f"\n*Voice Transcript:* \"{item['transcription']}\"\n")

    content = "\n".join(md)
    target_path = Path(output_path) if output_path else EXPORTS_DIR / f"Hostel_Haunt_Chronicle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(target_path)


def export_json_backup(output_path: Optional[str] = None, db_path: Optional[str] = None) -> str:
    """Exports full database as JSON."""
    data = {
        "metadata": {
            "app": "Hostel Haunt",
            "version": "1.0.0",
            "exported_at": datetime.now().isoformat(),
        },
        "night_watch": get_all_night_watches(db_path),
        "exam_haunt": get_all_exam_haunts(db_path),
        "memory_vault": get_all_memories(db_path),
        "family_echoes": get_all_family_echoes(db_path),
    }
    target_path = Path(output_path) if output_path else EXPORTS_DIR / f"hostel_haunt_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return str(target_path)
