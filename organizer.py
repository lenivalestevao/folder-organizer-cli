#!/usr/bin/env python3
# Folder Organizer CLI — sorts files in a folder into category subfolders.

import argparse, json, shutil
from pathlib import Path
from datetime import datetime

CATEGORIES = {
  "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"},
  "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
  "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
  "Videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
  "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
  "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
  "Code": {".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".cs", ".php", ".json"},
}
LOG_NAME = ".organizer_log.json"


def categorize(path):
  ext = path.suffix.lower()
  matches = [name for name, exts in CATEGORIES.items() if ext in exts]
  return matches[0] if matches else "Others"


def organize(target, dry_run):
  if not target.is_dir():
    raise SystemExit(f"Not a folder: {target}")
  moves = [(item, target / categorize(item) / item.name, categorize(item)) for item in sorted(target.iterdir()) if not item.is_dir() and item.name != LOG_NAME]
  if not moves:
    print("Nothing to organize — folder is already tidy.")
    return
  for source, dest, category in moves:
    prefix = "[dry-run] " if dry_run else ""
    print(f"{prefix}{source.name} -> {category}/")
    if not dry_run:
      dest.parent.mkdir(exist_ok=True)
      shutil.move(str(source), str(dest))
  if dry_run:
    print(f"\n{len(moves)} file(s) would be moved. Re-run without --dry-run to apply.")
    return
  log_path = target / LOG_NAME
  log_entries = json.loads(log_path.read_text()) if log_path.exists() else []
  log_entries.append({"timestamp": datetime.now().isoformat(), "moves": [{"from": str(s), "to": str(d)} for s, d, _ in moves]})
  log_path.write_text(json.dumps(log_entries, indent=2))
  print(f"\nDone — {len(moves)} file(s) organized. Run with --undo to reverse this.")


def undo(target):
  log_path = target / LOG_NAME
  if not log_path.exists():
    raise SystemExit("No organizer log found — nothing to undo.")
  log_entries = json.loads(log_path.read_text())
  if not log_entries:
    raise SystemExit("Log is empty — nothing to undo.")
  last_run = log_entries.pop()
  for move in reversed(last_run["moves"]):
    source = Path(move["to"])
    dest = Path(move["from"])
    if source.exists():
      dest.parent.mkdir(parents=True, exist_ok=True)
      shutil.move(str(source), str(dest))
      print(f"Restored {dest.name}")
  if log_entries:
    log_path.write_text(json.dumps(log_entries, indent=2))
  else:
    log_path.unlink()
  print("\nUndo complete.")


def main():
  parser = argparse.ArgumentParser(description="Organize a folder into category subfolders.")
  parser.add_argument("folder", type=Path, help="Folder to organize")
  parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
  parser.add_argument("--undo", action="store_true", help="Undo the last organize run")
  args = parser.parse_args()
  target = args.folder.expanduser().resolve()
  if args.undo:
    undo(target)
  else:
    organize(target, dry_run=args.dry_run)


if __name__ == "__main__":
  main()
