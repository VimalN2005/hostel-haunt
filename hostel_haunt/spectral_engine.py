"""Spectral Intelligence Engine for Hostel Haunt.

Bridges open-weight models (Gemma 2, Llama 3.2 via Ollama) with a resilient
procedural fallback engine so the application runs offline, locally, or in the cloud.
"""

import json
import logging
import random
from typing import Dict, Any, Optional
import requests
from hostel_haunt.config import OLLAMA_HOST, DEFAULT_MODEL, FALLBACK_MODE

logger = logging.getLogger(__name__)


class SpectralEngine:
    """Manages the 4 spectral voices of Hostel Haunt."""

    def __init__(self, model_name: str = DEFAULT_MODEL, host: str = OLLAMA_HOST):
        self.model_name = model_name
        self.host = host.rstrip("/")

    def _call_ollama(self, prompt: str, system_prompt: str) -> Optional[str]:
        """Attempts to generate text from a local Ollama instance with open-weights."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
            },
        }
        try:
            resp = requests.post(url, json=payload, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "").strip()
        except Exception as e:
            logger.debug("Local Ollama not reachable (%s), using procedural spectral engine.", e)
        return None

    # --- Persona 1: The Corridor Specter (Night Watch) ---

    def weave_night_tale(self, title: str, location: str, sensory_details: str, spook_level: int = 7) -> str:
        """Converts strange nocturnal hostel events into a chilling ghost story."""
        system_prompt = (
            "You are the Corridor Specter, an ancient spirit haunting an Indian engineering college hostel. "
            "You speak in gothic, eerie whispers, blending flickering fluorescent tubes, creaking ceiling fans, "
            "cold corridor drafts, and 3 AM isolation with the user's real hostel experience."
        )
        prompt = (
            f"Event Title: {title}\n"
            f"Location in Hostel: {location}\n"
            f"Atmospheric Details: {sensory_details}\n"
            f"Spook Intensity: {spook_level}/10\n\n"
            "Weave a haunting 2-3 paragraph spectral chronicle about this event. "
            "Capture the eerie feeling of a dark hostel wing at 3 AM."
        )

        ollama_result = self._call_ollama(prompt, system_prompt)
        if ollama_result:
            return ollama_result

        # Procedural Gothic Fallback
        intros = [
            f"The clock in the central quad had stopped at 3:17 AM when the air near {location} turned biting cold.",
            f"They say Wing 4 never truly sleeps, but tonight, the silence around {location} was thicker than grease.",
            f"A solitary yellow bulb hummed outside {location}, casting shadows that lingered a heartbeat too long.",
        ]
        mid_tones = [
            f"Every creak of the floorboards echoed {sensory_details}. It wasn't the wind—wind doesn't pause to listen before slipping under the wooden door.",
            f"The hostel mess had powered down hours ago, yet the scent of burnt kerosene and damp plaster hung heavy. {sensory_details} rattled the rusted locker hinges.",
            f"You could hear the low frequency drone that only tired engineers notice after staring at code for ten hours straight. But this was different: {sensory_details}.",
        ]
        conclusions = [
            f"If you walk past {location} tomorrow before dawn, do not glance at the foggy window. Some echoes do not want to be disturbed.",
            f"The night watchman swore he saw a silhouette standing still right there. When he flashed his torch, only {title} remained in the dust.",
            f"Keep your desk lamp burning. In this hostel, old memories don't fade; they just pace the empty corridors waiting for someone to stay awake.",
        ]

        return f"{random.choice(intros)}\n\n{random.choice(mid_tones)}\n\n{random.choice(conclusions)}"

    # --- Persona 2: The Backlog Phantom (Exam Haunt) ---

    def summon_exam_prophecy(
        self, subject: str, target_score: float, current_score: float, hours_slept: float, backlog_status: str
    ) -> Dict[str, str]:
        """Delivers a darkly humorous, deeply urgent wake-up call & spectral action plan."""
        system_prompt = (
            "You are the Backlog Phantom, the ghost of a legendary 2004 engineering batch senior who failed his End-Sems "
            "because of Procrastination and 4 AM gaming. Now your spirit roams the library to save juniors from academic doom."
        )
        prompt = (
            f"Subject: {subject}\n"
            f"Current Prep/Score: {current_score} | Target: {target_score}\n"
            f"Hours Slept: {hours_slept} hours\n"
            f"Backlog Status: {backlog_status}\n\n"
            "Deliver a sharp spectral warning and a 3-step ruthless action plan to survive the exam."
        )

        ollama_result = self._call_ollama(prompt, system_prompt)
        if ollama_result:
            return {
                "warning": ollama_result,
                "action_plan": "1. Drink black coffee and review unit 1-3 PYQs.\n2. Exorcise your phone until sunrise.\n3. Sleep 4 hours to avoid cognitive freeze.",
            }

        # Procedural Urgent Academic Warning
        urgency = "CRITICAL COGNITIVE COLLAPSE" if hours_slept < 4 else "DANGEROUS PROCRASTINATION"
        warning = (
            f"⚠️ SPECTRAL MANIFESTATION [{urgency}]:\n"
            f"I see you staring at '{subject}', mortal. In the winter of 2004, I too thought 3 hours of sleep and YouTube 1-shot marathons "
            f"could conquer a 60-mark paper. Now I am a ghost trapped behind the reference bookshelf in Section C!\n\n"
            f"You are sitting at {current_score} aiming for {target_score}. If you don't shut down the endless reels and confront the syllabus, "
            f"the examiner's red pen will haunt your semester transcript for the next four years."
        )

        action_plan = (
            f"📜 THE GHOST SENIOR'S SURVIVAL DIRECTIVE:\n"
            f"1. Zero-Hour Triage: Pick the 2 heaviest-weighted units in '{subject}' and master their derivations first.\n"
            f"2. Digital Exorcism: Toss your smartphone inside the rusted steel almirah until 8:00 AM.\n"
            f"3. Fuel the Vessel: Take a 20-minute power nap, drink hot water or mess tea, and secure those passing marks!"
        )

        return {"warning": warning, "action_plan": action_plan}

    # --- Persona 3: The Memory Guardian (Memory Vault - Día de los Muertos) ---

    def crystallize_memory(self, title: str, category: str, raw_notes: str, emotion_tags: str) -> str:
        """Transforms unpolished hostel banter into an enduring, lyrical college memoir."""
        system_prompt = (
            "You are the Guardian of the Hostel Altar, channeling the spirit of Día de los Muertos. "
            "You honor the transient beauty of college life—the brotherhood, the late-night tea stalls, "
            "the borrowed sweaters, the laughter that echoes long after students graduate."
        )
        prompt = (
            f"Memory Title: {title}\n"
            f"Category: {category}\n"
            f"Raw Experience: {raw_notes}\n"
            f"Emotions: {emotion_tags}\n\n"
            "Write a poetic, nostalgic memoir capturing this fleeting hostel memory so it is never lost."
        )

        ollama_result = self._call_ollama(prompt, system_prompt)
        if ollama_result:
            return ollama_result

        # Procedural Poetic Memoir
        return (
            f"🕯️ *The Altar of {title.upper()}* 🕯️\n\n"
            f"Years from today, when the hostel gates are far behind and corporate calendars blur the seasons, "
            f"this fragment from the {category} will remain glowing like a marigold petal on stone.\n\n"
            f"'{raw_notes.strip()}'\n\n"
            f"It was never just about surviving the semester. It was about shared Maggi at 2 AM, the songs played on cracked phone speakers, "
            f"and the unspoken promise that no one in this room fought the world alone. "
            f"This memory is sealed in the vault; time cannot wither what the heart has revered."
        )

    # --- Persona 4: The Ancestral Hearth (Family Echoes) ---

    def honor_family_voice(self, member: str, relation: str, note_or_blessing: str) -> str:
        """Reflects upon family love with sacred remembrance and heartfelt comfort."""
        system_prompt = (
            "You are the Ancestral Hearth spirit. You understand the quiet sacrifice of parents and families "
            "who send their children away to college hostels. You provide grounding warmth and emotional strength."
        )
        prompt = (
            f"Family Member: {member} ({relation})\n"
            f"Their Words / Blessing: {note_or_blessing}\n\n"
            "Write a touching reflection honoring this connection and blessing."
        )

        ollama_result = self._call_ollama(prompt, system_prompt)
        if ollama_result:
            return ollama_result

        # Procedural Heartfelt Reflection
        return (
            f"🌼 *Blessing of the Hearth: {member} ({relation})* 🌼\n\n"
            f"Miles away from home, in a quiet hostel room where loneliness sometimes knocks on the door, "
            f"these words carry the warmth of a mother's kitchen and an ancestor's prayer.\n\n"
            f"\"{note_or_blessing.strip()}\"\n\n"
            f"Never forget the roots that sustain your journey. When exams press heavy and the night feels endless, "
            f"remember you are carrying the hopes of those who love you without condition. The flame burns bright for you."
        )
