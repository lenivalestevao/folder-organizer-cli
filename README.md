# 📂 Folder Organizer CLI

A tiny, zero-dependency Python script that cleans up a messy folder — like your Downloads folder — by sorting files into category subfolders (Images, Documents, Videos, Audio, Archives, Code, Others). Safe by default: preview what would happen before anything moves, and undo in one command if you change your mind.

<br/>

## ✨ Why

Most of us have a Downloads folder with 500 files in it. This script sorts it out in a second, without needing to install anything beyond Python itself.

<br/>

## 🚀 Usage

```bash
# Preview what would happen (nothing is moved)
python organizer.py ~/Downloads --dry-run

# Actually organize the folder
python organizer.py ~/Downloads

# Changed your mind? Undo the last run
python organizer.py ~/Downloads --undo
```

<br/>

## 📁 What it does

🔹 Scans the target folder (top level only, your subfolders are left alone)<br/>
🔹 Groups files by extension into categories: Images, Documents, Spreadsheets, Videos, Audio, Archives, Code, Others<br/>
🔹 Skips files already inside a category folder, so it's safe to run more than once<br/>
🔹 Writes a log of every move to `.organizer_log.json` in the target folder<br/>
🔹 `--undo` reads that log and moves every file back to exactly where it came from

<br/>

## 🛠️ Requirements

Python 3.8+. No third-party packages — just the standard library.

<br/>

## 🤝 Contributing

Pull requests welcome — new categories, better extension detection, a `--config` file for custom rules, etc.

<br/>

## 📄 License

MIT — see [LICENSE](LICENSE).
