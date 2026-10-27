"""Hostel Haunt - The ghost that lives in your laptop.

Interactive Streamlit Application for Hacktoberfest 2026 Week 4 DEV Challenge.
Unifies Halloween Spookiness with Día de los Muertos Sacred Remembrance.
"""

import os
import streamlit as st
from datetime import datetime

from hostel_haunt import db
from hostel_haunt.spectral_engine import SpectralEngine
from hostel_haunt.audio_bridge import AudioBridge
from hostel_haunt.exporters import export_markdown_chronicle, export_json_backup
from hostel_haunt.config import APP_TITLE, APP_SUBTITLE

# Streamlit Page Config
st.set_page_config(
    page_title="Hostel Haunt 🕯️👻",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Gothic & Marigold Styling
st.markdown(
    """
    <style>
    /* Dark Gothic & Candle Glow Theme */
    .stApp {
        background-color: #0d0f12;
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .spooky-header {
        text-align: center;
        padding: 1.5rem 0;
        background: radial-gradient(circle, rgba(255, 120, 0, 0.15) 0%, rgba(13, 15, 18, 0) 70%);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .spooky-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff9900, #ff4d4d, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .spooky-subtitle {
        color: #8b949e;
        font-size: 1.1rem;
        font-style: italic;
    }
    .card-ghost {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #ff4d4d;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .card-altar {
        background-color: #1a1612;
        border: 1px solid #4d3800;
        border-left: 4px solid #ff9900;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .card-academic {
        background-color: #111a19;
        border: 1px solid #1f423f;
        border-left: 4px solid #00ffcc;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .candle-active {
        color: #ffaa00;
        text-shadow: 0 0 10px #ff7700;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def seed_sample_data_if_empty():
    """Populates evocative sample lore if the database is newly initialized."""
    if len(db.get_all_night_watches()) == 0:
        db.add_night_watch(
            title="The 3:17 AM Dripping Tap of Wing 3",
            location="Wing 3 Common Washroom",
            sensory_details="A rhythmically dripping rusted brass tap. Fluorescent light buzzing like angry wasps.",
            generated_story=(
                "The clock in the central quad had stopped at 3:17 AM when the air near Wing 3 Common Washroom turned biting cold.\n\n"
                "Every creak of the floorboards echoed like an old typewriter key. It wasn't plumbing—plumbing doesn't hesitate "
                "before dripping in sync with your heartbeat. When students peered through the foggy mirrors, the condensation "
                "had already formed the shape of an outstretched hand.\n\n"
                "If you walk past Wing 3 tonight, do not look into the mirror under the buzzing light. Some memories pace the tiles forever."
            ),
            spook_rating=8,
            tags="hostel,night,creepy",
        )

    if len(db.get_all_exam_haunts()) == 0:
        db.add_exam_haunt(
            subject="Operating Systems (Deadlocks & Memory Management)",
            target_score=85.0,
            current_score=38.0,
            hours_slept=2.5,
            backlog_status="danger",
            spectral_warning=(
                "⚠️ SPECTRAL MANIFESTATION [CRITICAL COGNITIVE COLLAPSE]:\n"
                "I see you staring at Operating Systems, mortal. In 2004, I too thought 2.5 hours of sleep and coffee powder mixed in cold water "
                "could conquer Banker's Algorithm. Now I am a phantom trapped behind the reference racks in Section C!\n\n"
                "You are sitting at 38 aiming for 85. If you do not close your phone, the examiner's red fountain pen will strike like thunder."
            ),
            action_plan=(
                "📜 THE GHOST SENIOR'S SURVIVAL DIRECTIVE:\n"
                "1. Master Semaphore vs Mutex and Banker's Algorithm derivations immediately.\n"
                "2. Lock your smartphone inside the steel cupboard until morning.\n"
                "3. Take a 25-minute power nap to prevent memory segmentation faults in your brain."
            ),
        )

    if len(db.get_all_memories()) == 0:
        db.add_memory(
            title="Late Night Tapri Chai Before Placements",
            category="Hostel Banter & Placements",
            raw_notes="Sitting with Aman and Rohit on the broken stone bench outside the back gate at 2:30 AM, sipping half-cutting chai and sharing cheap biscuits after getting rejected in the first round.",
            polished_memoir=(
                "🕯️ *The Altar of LATE NIGHT TAPRI CHAI BEFORE PLACEMENTS* 🕯️\n\n"
                "Years from today, when corporate calendars blur the seasons and high-rise apartments replace steel cots, "
                "this half-cutting cup of tea will still warm your soul like a golden marigold petal on stone.\n\n"
                "It was never just about passing the coding interview. It was about sitting on cold stone together, laughing through "
                "the rejection, and knowing that as long as the kettle was boiling, no one in this hostel was left behind."
            ),
            emotion_tags="brotherhood,hope,chai",
            candle_color="#ff9900",
        )

    if len(db.get_all_family_echoes()) == 0:
        db.add_family_echo(
            family_member="Maa",
            relation="Mother",
            blessing_or_note="Beta, hostel me theek se khana khate rehna. Padhai ke chakkar me tabiyat mat kharab karna. Bhagwan hamesha tumhare sath hai.",
            candle_lit=1,
            transcription="Beta, khana time pe kha lena aur zyada raat tak mat jaagna. Hum sab theek hain yahan, tum bas acche se padhai karna.",
        )


# Initialize DB and seed
db.init_db()
seed_sample_data_if_empty()
engine = SpectralEngine()
audio_bridge = AudioBridge()

# Header
st.markdown(
    f"""
    <div class="spooky-header">
        <div class="spooky-title">{APP_TITLE}</div>
        <div class="spooky-subtitle">"{APP_SUBTITLE}"</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.markdown("### 🕯️ Spectral Gateway")
    st.markdown(
        """
        **Hostel Haunt** connects the spooky mysteries of hostel life with the sacred remembrance of **Día de los Muertos**.
        """
    )
    st.markdown("---")
    st.markdown("#### ⚡ Open-Weight Engine")
    st.info(f"Model: `{engine.model_name}`\nHost: `{engine.host}`\nFallback: `Active & Resilient`")
    
    st.markdown("---")
    st.markdown("#### 📊 Quick Altar Stats")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("🌙 Nights", len(db.get_all_night_watches()))
        st.metric("🌼 Memories", len(db.get_all_memories()))
    with col_s2:
        st.metric("📚 Exams", len(db.get_all_exam_haunts()))
        st.metric("🧡 Echoes", len(db.get_all_family_echoes()))

    st.markdown("---")
    st.caption("Built with ❤️ by **Vimal Sahani** for Hacktoberfest 2026 Week 4.")


# Navigation Tabs
tab_night, tab_exam, tab_memory, tab_family, tab_chronicles = st.tabs([
    "🌙 Night Watch (Ghost Stories)",
    "📚 Exam Haunt (Academic Dread)",
    "🌼 Memory Vault (Día de los Muertos)",
    "🧡 Family Echoes (Voice Altars)",
    "📜 Sacred Chronicles & Export",
])

# ----------------- TAB 1: NIGHT WATCH -----------------
with tab_night:
    st.subheader("🌙 Night Watch: Nocturnal Hostel Lore")
    st.markdown(
        "Did you hear strange footsteps in Wing 4? A flickering light or a mysterious power outage at 3 AM? "
        "Feed the raw event to the **Corridor Specter** to weave it into local folklore."
    )

    with st.expander("👻 Summon a New Ghost Story from the Night", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            n_title = st.text_input("Event Title", placeholder="e.g., The 3:15 AM Mess Cooler Shadow")
            n_loc = st.text_input("Location in Hostel", placeholder="e.g., 2nd Floor Mess Corridor / Room 304")
            n_details = st.text_area(
                "Atmospheric / Sensory Details",
                placeholder="e.g., Cold sudden breeze, sound of water dripping, steel plate rattling on table...",
                height=100,
            )
        with col2:
            n_spook = st.slider("Spook Intensity (1 - 10)", min_value=1, max_value=10, value=7)
            n_tags = st.text_input("Tags", value="hostel,night,haunted")
            submit_night = st.button("🕯️ Awaken the Specter", type="primary", use_container_width=True)

        if submit_night:
            if not n_title or not n_details:
                st.warning("Please provide a title and atmospheric details for the ghost.")
            else:
                with st.spinner("The corridors are creaking... weaving your story..."):
                    story = engine.weave_night_tale(n_title, n_loc, n_details, n_spook)
                    db.add_night_watch(n_title, n_loc, n_details, story, n_spook, n_tags)
                    st.success("The nocturnal chronicle has been permanently etched into the walls!")
                    st.rerun()

    st.markdown("### 📖 Recorded Nocturnal Chronicles")
    night_records = db.get_all_night_watches()
    if not night_records:
        st.info("The corridors are peaceful for now. No ghosts recorded.")
    else:
        for item in night_records:
            st.markdown(
                f"""
                <div class="card-ghost">
                    <h4>👻 {item['title']} <span style="font-size:0.8rem; color:#8b949e;">({item['location']}) — Spook: {item['spook_rating']}/10</span></h4>
                    <p style="font-size:0.85rem; color:#8b949e;">Recorded: {item['timestamp']}</p>
                    <p style="line-height:1.6; white-space: pre-wrap;">{item['generated_story']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------- TAB 2: EXAM HAUNT -----------------
with tab_exam:
    st.subheader("📚 Exam Haunt: The Backlog Phantom's Triage")
    st.markdown(
        "Afraid of tomorrow's paper? Procrastinating on Instagram reels while your syllabus mocks you? "
        "Consult the **Backlog Phantom**—the spirit of a 2004 batch senior who failed so you don't have to."
    )

    with st.expander("⚠️ Summon Academic Triage", expanded=True):
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            e_subject = st.text_input("Subject / Course", placeholder="e.g., Computer Networks / Compiler Design")
            e_backlog = st.selectbox("Backlog Risk Status", ["Low (Passing is certain)", "Moderate (Scared)", "Severe (Zero prep / Panic)"])
        with col_e2:
            e_target = st.number_input("Target Marks (out of 100)", min_value=30.0, max_value=100.0, value=75.0)
            e_current = st.number_input("Estimated Current Prep Score", min_value=0.0, max_value=100.0, value=35.0)
        with col_e3:
            e_sleep = st.number_input("Hours Slept Last Night", min_value=0.0, max_value=14.0, value=3.0, step=0.5)
            submit_exam = st.button("⚡ Summon Senior Ghost", type="primary", use_container_width=True)

        if submit_exam:
            if not e_subject:
                st.warning("Please specify the subject that is haunting you.")
            else:
                with st.spinner("The library stacks are rumbling with ancient PYQ papers..."):
                    prophecy = engine.summon_exam_prophecy(e_subject, e_target, e_current, e_sleep, e_backlog)
                    db.add_exam_haunt(
                        e_subject, e_target, e_current, e_sleep, e_backlog, prophecy["warning"], prophecy["action_plan"]
                    )
                    st.success("The Senior Ghost has spoken! Follow the survival directive.")
                    st.rerun()

    st.markdown("### 📜 Prophecies & Survival Directives")
    exam_records = db.get_all_exam_haunts()
    if not exam_records:
        st.info("No active exam hauntings logged yet.")
    else:
        for ex in exam_records:
            st.markdown(
                f"""
                <div class="card-academic">
                    <h4>⚠️ {ex['subject']} <span style="font-size:0.85rem; color:#8b949e;">(Target: {ex['target_score']} | Prep: {ex['current_score']} | Sleep: {ex['hours_slept']}h)</span></h4>
                    <p style="white-space: pre-wrap; color:#e6edf3;">{ex['spectral_warning']}</p>
                    <hr style="border-color:#1f423f;">
                    <p style="white-space: pre-wrap; color:#00ffcc; font-weight:500;">{ex['action_plan']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------- TAB 3: MEMORY VAULT -----------------
with tab_memory:
    st.subheader("🌼 Memory Vault: The Día de los Muertos Altar")
    st.markdown(
        "Hostel life is fleeting. The midnight birthdays, shared noodles, heated debate on room verandahs—"
        "once you graduate, these rooms will belong to someone else. **Preserve your memories upon the virtual altar.**"
    )

    with st.expander("🕯️ Place a Memory Upon the Altar", expanded=True):
        m_title = st.text_input("Memory Title", placeholder="e.g., The Night We Fixed the Final Year Project at 4 AM")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            m_cat = st.selectbox(
                "Category",
                ["Hostel Room Banter", "Late Night Tapri & Mess", "Wing Traditions", "Farewell & Nostalgia", "Campus Walks"],
            )
        with col_m2:
            m_emotions = st.text_input("Emotion Tags", value="friendship,gratitude,nostalgia")

        m_notes = st.text_area(
            "Raw Memory Notes",
            placeholder="Write freely: who was there, what song was playing, what joke was cracked...",
            height=120,
        )
        submit_mem = st.button("🌼 Crystallize into Sacred Memoir", type="primary", use_container_width=True)

        if submit_mem:
            if not m_title or not m_notes:
                st.warning("Please provide a title and memory description.")
            else:
                with st.spinner("Adorning with virtual marigold petals and soft candle flame..."):
                    memoir = engine.crystallize_memory(m_title, m_cat, m_notes, m_emotions)
                    db.add_memory(m_title, m_cat, m_notes, memoir, m_emotions)
                    st.success("Your memory is now eternal in the vault.")
                    st.rerun()

    st.markdown("### 🕯️ The Living Altar of College Memories")
    mem_records = db.get_all_memories()
    if not mem_records:
        st.info("The altar is waiting for your first college memory.")
    else:
        for mem in mem_records:
            st.markdown(
                f"""
                <div class="card-altar">
                    <h4>🌼 {mem['title']} <span style="font-size:0.8rem; color:#ff9900;">[{mem['category']}]</span></h4>
                    <p style="font-size:0.85rem; color:#8b949e;">Tags: {mem['emotion_tags']} | Recorded: {mem['timestamp']}</p>
                    <p style="white-space: pre-wrap; font-style:italic; line-height:1.6;">{mem['polished_memoir']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ----------------- TAB 4: FAMILY ECHOES -----------------
with tab_family:
    st.subheader("🧡 Family Echoes: The Ancestral Hearth")
    st.markdown(
        "Living hundreds of miles away in a hostel room, nothing grounds a student more than the voice of home. "
        "Keep your parents' and loved ones' voice notes and blessings alive. **Light a candle to honor them.**"
    )

    with st.expander("🕯️ Add a Family Voice Note / Blessing", expanded=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            f_member = st.text_input("Family Member Name", placeholder="e.g., Papa, Dadi, Didi")
            f_rel = st.text_input("Relation", placeholder="e.g., Father, Grandmother, Sister")
        with col_f2:
            f_audio = st.file_uploader("Upload Voice Note (WAV / MP3 / M4A / OGG)", type=["wav", "mp3", "m4a", "ogg"])
            f_hint = st.text_input("Quick Transcript / Key Words (Optional)", placeholder="e.g., Call me when you reach...")

        f_blessing = st.text_area(
            "Blessing, Advice, or Sacred Words",
            placeholder="e.g., 'Apna dhyan rakhna, sab theek hoga.'",
            height=80,
        )
        submit_echo = st.button("🔥 Light Altar Candle & Save Echo", type="primary", use_container_width=True)

        if submit_echo:
            if not f_member or not f_blessing:
                st.warning("Please specify the family member and their blessing or advice.")
            else:
                with st.spinner("Lighting the candle and recording the echo..."):
                    audio_path = ""
                    transcription = ""
                    if f_audio:
                        audio_path = audio_bridge.save_audio_file(f_audio, f_audio.name)
                        transcription_res = audio_bridge.transcribe(audio_path, simulated_hint=f_hint or f_blessing)
                        transcription = transcription_res.get("text", "")
                    elif f_hint:
                        transcription = f_hint

                    db.add_family_echo(
                        f_member, f_rel, f_blessing, audio_path=audio_path, candle_lit=1, transcription=transcription
                    )
                    st.success("The ancestral flame has been lit for your loved one.")
                    st.rerun()

    st.markdown("### 🔥 Living Family Altars")
    echo_records = db.get_all_family_echoes()
    if not echo_records:
        st.info("No family echoes added yet.")
    else:
        for echo in echo_records:
            candle_status = "🔥 Candle Burning" if echo["candle_lit"] else "🕯️ Candle Unlit"
            col_e_a, col_e_b = st.columns([4, 1])
            with col_e_a:
                st.markdown(
                    f"""
                    <div class="card-altar">
                        <h4>🌼 {echo['family_member']} ({echo['relation']}) — <span class="candle-active">{candle_status}</span></h4>
                        <p style="font-size:1.05rem; font-style:italic; color:#ffd280;">"{echo['blessing_or_note']}"</p>
                        {f'<p style="font-size:0.85rem; color:#8b949e;"><b>Voice Transcript:</b> {echo["transcription"]}</p>' if echo.get("transcription") else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_e_b:
                btn_label = "Extinguish 🕯️" if echo["candle_lit"] else "Relight 🔥"
                if st.button(btn_label, key=f"toggle_{echo['id']}", use_container_width=True):
                    db.toggle_candle(echo["id"])
                    st.rerun()

# ----------------- TAB 5: CHRONICLES & EXPORT -----------------
with tab_chronicles:
    st.subheader("📜 Sacred Chronicles & Full Data Export")
    st.markdown(
        "Generate a complete archival book of your hostel haunting, or export a local JSON backup. "
        "No cloud lock-in—100% of your data stays on your machine."
    )

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("📖 Generate Markdown Chronicle Book", use_container_width=True, type="primary"):
            exported_file = export_markdown_chronicle()
            st.success(f"Chronicle generated: `{exported_file}`")
            with open(exported_file, "r", encoding="utf-8") as f:
                chronicle_content = f.read()
            st.download_button(
                "📥 Download Markdown Chronicle",
                data=chronicle_content,
                file_name="Hostel_Haunt_Chronicle.md",
                mime="text/markdown",
                use_container_width=True,
            )

    with col_exp2:
        if st.button("💾 Export Complete JSON Backup", use_container_width=True):
            json_file = export_json_backup()
            st.success(f"JSON backup exported: `{json_file}`")
            with open(json_file, "r", encoding="utf-8") as f:
                json_content = f.read()
            st.download_button(
                "📥 Download JSON Archive",
                data=json_content,
                file_name="hostel_haunt_archive.json",
                mime="application/json",
                use_container_width=True,
            )

    st.markdown("---")
    st.markdown("### 👁️ Live Chronicle Preview")
    try:
        preview_file = export_markdown_chronicle()
        with open(preview_file, "r", encoding="utf-8") as f:
            st.markdown(f.read())
    except Exception as e:
        st.warning(f"Unable to render preview: {e}")
