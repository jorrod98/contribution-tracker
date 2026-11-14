import json
from pathlib import Path
from typing import Any


def load_entries(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Data file is not valid JSON: {path}") from error

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"Data file must contain a JSON list of entries: {path}")
    return data


def save_entries(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

