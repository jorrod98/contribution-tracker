import argparse
from datetime import datetime, timezone
import sys
from pathlib import Path
from typing import Any, List, Optional
from uuid import uuid4
import webbrowser

from contribution_tracker.storage import load_entries, save_entries
from contribution_tracker.viewer import render_html

STATUSES = ("planned", "in-progress", "pr-open", "merged", "closed")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contribution-tracker",
        description="Track open-source issues and pull requests you want to work on.",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path(__file__).resolve().parent.parent / ".contribution-tracker.json",
        help="path to the local JSON data file",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="track an issue or pull request")
    add.add_argument("--repo", required=True, help="repository, such as owner/name")
    add.add_argument("--url", required=True, help="issue or pull request URL")
    add.add_argument("--title", required=True, help="short description")
    add.add_argument("--notes", default="", help="optional notes")

    commands.add_parser("list", help="show tracked contributions")
    commands.add_parser("view", help="open an HTML view in your browser")

    update = commands.add_parser("update", help="update a tracked contribution")
    update.add_argument("id", help="entry ID shown by the list command")
    update.add_argument("--status", choices=STATUSES)
    update.add_argument("--notes")
    return parser


def _add_entry(args: argparse.Namespace, entries: list[dict[str, Any]]) -> int:
    now = _timestamp()
    entry = {
        "id": uuid4().hex[:8],
        "repo": args.repo,
        "url": args.url,
        "title": args.title,
        "status": "planned",
        "notes": args.notes,
        "created_at": now,
        "updated_at": now,
    }
    entries.append(entry)
    save_entries(args.data_file, entries)
    print(f"Added {entry['id']}: {entry['title']}")
    return 0


def _list_entries(entries: list[dict[str, Any]]) -> int:
    if not entries:
        print("No contributions tracked yet.")
        return 0

    for entry in entries:
        print(
            f"{entry['id']}  [{entry['status']}]  {entry['repo']}  "
            f"{entry['title']}\n    {entry['url']}"
        )
        if entry.get("notes"):
            print(f"    Notes: {entry['notes']}")
    return 0


def _update_entry(args: argparse.Namespace, entries: list[dict[str, Any]]) -> int:
    if args.status is None and args.notes is None:
        print("Provide --status or --notes to update.", file=sys.stderr)
        return 2

    entry = next((item for item in entries if item.get("id") == args.id), None)
    if entry is None:
        print(f"No contribution found with ID {args.id}.", file=sys.stderr)
        return 1

    if args.status is not None:
        entry["status"] = args.status
    if args.notes is not None:
        entry["notes"] = args.notes
    entry["updated_at"] = _timestamp()
    save_entries(args.data_file, entries)
    print(f"Updated {entry['id']}.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)

    try:
        entries = load_entries(args.data_file)
        if args.command == "add":
            return _add_entry(args, entries)
        if args.command == "list":
            return _list_entries(entries)
        if args.command == "view":
            viewer_path = args.data_file.parent / ".contribution-tracker.html"
            viewer_path.parent.mkdir(parents=True, exist_ok=True)
            viewer_path.write_text(render_html(entries), encoding="utf-8")
            if not webbrowser.open(viewer_path.resolve().as_uri()):
                print(
                    f"Error: couldn't open the HTML viewer. Open {viewer_path} in a browser.",
                    file=sys.stderr,
                )
                return 1
            print(f"Opened tracker viewer: {viewer_path}")
            return 0
        return _update_entry(args, entries)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

