"""Command Line Interface for Hostel Haunt.

Run spectral rituals, summon ghosts, and export chronicles directly from your terminal.
"""

import argparse
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from hostel_haunt import db
from hostel_haunt.spectral_engine import SpectralEngine
from hostel_haunt.exporters import export_markdown_chronicle

console = Console(legacy_windows=False)


def main():
    parser = argparse.ArgumentParser(
        prog="hostel-haunt",
        description="Hostel Haunt: The ghost that lives in your laptop. (Hacktoberfest 2026 Week 4)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Spectral subcommands")

    # Command: night
    p_night = subparsers.add_parser("night", help="Record a strange nocturnal hostel event")
    p_night.add_argument("--title", required=True, help="Title of the strange event")
    p_night.add_argument("--location", default="Wing 4 corridor", help="Location in hostel")
    p_night.add_argument("--details", required=True, help="Sensory/atmospheric details")
    p_night.add_argument("--spook", type=int, default=7, help="Spook intensity (1-10)")

    # Command: exam
    p_exam = subparsers.add_parser("exam", help="Summon the Backlog Phantom for academic triage")
    p_exam.add_argument("--subject", required=True, help="Subject name")
    p_exam.add_argument("--target", type=float, default=85.0, help="Target marks / percentage")
    p_exam.add_argument("--score", type=float, default=45.0, help="Current preparation / score")
    p_exam.add_argument("--sleep", type=float, default=3.5, help="Hours slept last night")
    p_exam.add_argument("--backlog", default="at-risk", help="Backlog status")

    # Command: memory
    p_mem = subparsers.add_parser("memory", help="Preserve a college memory in the Día de los Muertos vault")
    p_mem.add_argument("--title", required=True, help="Memory title")
    p_mem.add_argument("--category", default="Wing Camaraderie", help="Category")
    p_mem.add_argument("--notes", required=True, help="Raw memory notes")
    p_mem.add_argument("--tags", default="hostel,nostalgia", help="Emotion tags")

    # Command: list
    subparsers.add_parser("list", help="List all recorded spectral entities")

    # Command: export
    p_export = subparsers.add_parser("export", help="Export the complete Spectral Chronicle in Markdown")
    p_export.add_argument("--out", default=None, help="Output path")

    args = parser.parse_args()

    db.init_db()
    engine = SpectralEngine()

    if args.command == "night":
        console.print("[bold red]🕯️ Summoning the Corridor Specter...[/bold red]")
        story = engine.weave_night_tale(args.title, args.location, args.details, args.spook)
        db.add_night_watch(args.title, args.location, args.details, story, args.spook)
        console.print(Panel(story, title=f"👻 {args.title} ({args.location})", border_style="red"))

    elif args.command == "exam":
        console.print("[bold yellow]📜 Consulting the Backlog Phantom...[/bold yellow]")
        res = engine.summon_exam_prophecy(args.subject, args.target, args.score, args.sleep, args.backlog)
        db.add_exam_haunt(args.subject, args.target, args.score, args.sleep, args.backlog, res["warning"], res["action_plan"])
        console.print(Panel(res["warning"], title=f"⚠️ Academic Dread: {args.subject}", border_style="yellow"))
        console.print(Panel(res["action_plan"], title="🛡️ Survival Directive", border_style="green"))

    elif args.command == "memory":
        console.print("[bold magenta]🌼 Placing memory upon the Virtual Altar...[/bold magenta]")
        memoir = engine.crystallize_memory(args.title, args.category, args.notes, args.tags)
        db.add_memory(args.title, args.category, args.notes, memoir, args.tags)
        console.print(Panel(memoir, title=f"🕯️ {args.title}", border_style="magenta"))

    elif args.command == "list":
        table = Table(title="🕯️ Hostel Haunt: Active Spectral Records")
        table.add_column("Dimension", style="cyan")
        table.add_column("Count", style="green")
        table.add_row("Night Watch Chronicles", str(len(db.get_all_night_watches())))
        table.add_row("Exam Haunt Prophecies", str(len(db.get_all_exam_haunts())))
        table.add_row("Memory Vault Altars", str(len(db.get_all_memories())))
        table.add_row("Family Echoes", str(len(db.get_all_family_echoes())))
        console.print(table)

    elif args.command == "export":
        out_file = export_markdown_chronicle(args.out)
        console.print(f"[bold green]✨ Spectral chronicle exported successfully to:[/bold green] {out_file}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
