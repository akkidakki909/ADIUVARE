from pathlib import Path
from typing import Any

import yaml


def merge_sections(path: str | Path, changes: dict[str, Any]) -> dict[str, Any]:
    file_path = Path(path)
    raw = _read_yaml(file_path)
    _merge(raw, changes)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return raw


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return loaded if isinstance(loaded, dict) else {}


def _merge(base: dict[str, Any], changes: dict[str, Any]) -> None:
    for key, val in changes.items():
        if isinstance(base.get(key), dict) and isinstance(val, dict):
            _merge(base[key], val)
        else:
            base[key] = val
