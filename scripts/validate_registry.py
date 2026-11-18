#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data = json.loads((root / "registry.json").read_text(encoding="utf-8"))

assert data.get("schema_version") == 1, "schema_version must be 1"
exts = data.get("extensions")
assert isinstance(exts, list) and len(exts) > 0, "extensions must be a non-empty list"

seen_ids = set()
required = {"id", "name", "description", "repo", "latest_version", "file_extensions", "languages", "tools"}
for entry in exts:
    missing = required - set(entry.keys())
    assert not missing, f"entry {entry.get('id')} missing fields: {missing}"
    ext_id = entry["id"]
    assert ext_id not in seen_ids, f"duplicate extension id: {ext_id}"
    seen_ids.add(ext_id)
    assert entry["repo"].startswith("https://github.com/koren-idep/"), f"unexpected repo url: {entry['repo']}"
    assert isinstance(entry["file_extensions"], list) and entry["file_extensions"], f"{ext_id} must list file_extensions"

print(f"Validated {len(exts)} extensions in registry.json")
