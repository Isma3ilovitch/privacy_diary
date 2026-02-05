# The Privacy Diary - Terminal Edition Setup Guide

## 🎯 Overview
A simple, terminal-based journaling app with local AI analysis.
**No GUI, no web interface - just pure command-line.**

---

## 📋 Prerequisites


- **Python 3.9+**
- **Ollama** installed
- **~4GB free RAM** (for running small LLM models)

---

## 🚀 Quick Start

### Step 1: Install Ollama

```bash
# Install via Homebrew
brew install ollama

# Start Ollama service (in separate terminal)
ollama serve
```

### Step 2: Download AI Model

```bash
# Download Llama 3 (recommended)
ollama pull llama3
```

### Step 3: Install Python Dependencies

```bash
# Install required packages
pip install cryptography ollama

# OR use requirements file:
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
# Make executable (optional)
chmod +x privacy_diary_terminal.py

# Run it
python3 privacy_diary_terminal.py
```

---

## 📖 How to Use

### Main Menu

When you start the app, you'll see:

```
╔══════════════════════════════════════════════════════════╗
║         🔒  THE PRIVACY DIARY - TERMINAL EDITION        ║
╚══════════════════════════════════════════════════════════╝

100% Local • Fully Encrypted • Offline AI

MAIN MENU:
  1. Write new entry
  2. View recent entries
  3. Check system status
  4. Exit
```

### Writing an Entry

1. Select option **1**
2. Start typing your journal entry
3. When done, type **END** on a new line
4. Choose if you want AI analysis **(Y/n)**
5. Choose if you want to save **(Y/n)**

**Example:**
```
Select option [1-4]: 1

═══ NEW JOURNAL ENTRY ═══

Write your thoughts below. When done, type 'END' on a new line:

Today was amazing! I finally finished my project.
I feel so accomplished and ready for the next challenge.
END

📝 Entry written: 14 words

Would you like AI analysis of this entry?
[Y/n]: y

🤔 Analyzing your entry locally...

═══ AI ANALYSIS ═══

That's wonderful! Completing a project is a significant achievement, 
and you should feel proud of yourself. Keep that momentum going!

Save this entry? (will be encrypted with AES-128)
[Y/n]: y

✅ Entry saved successfully!
🔒 Encrypted and stored at: /Users/you/.privacy_diary/diary_entries.enc
📊 Total entries: 1
```

### Viewing Recent Entries

1. Select option **2**
2. See your 5 most recent entries
3. Each shows: date, time, and preview

**Example:**
```
═══ RECENT ENTRIES ═══

1. February 05, 2026 at 02:30 PM
Today was amazing! I finally finished my project...

2. February 04, 2026 at 09:15 AM
Woke up feeling grateful for another day...

📊 Showing 2 of 2 total entries
```

### Checking Status

1. Select option **3**
2. See Ollama status, storage info, and privacy status

**Example:**
```
═══ SYSTEM STATUS ═══

✅ Ollama: Running
   Model: llama3
   Host: localhost:11434

✅ Storage: Encrypted
   Location: /Users/you/.privacy_diary
   Entries: 5
   Encryption: AES-128 (Fernet)

✅ Privacy: Protected
   100% Local Processing
   No Cloud Connection
   No Tracking or Telemetry
```

### Exiting

1. Select option **4**
2. Or press **Ctrl+C** anytime

---

## ⌨️ Features

### ✅ What It Does

- **Write journal entries** in the terminal
- **AI sentiment analysis** with supportive feedback
- **AES-128 encryption** for all saved entries
- **View recent entries** with previews
- **System status check** for Ollama and storage
- **Color-coded output** for better readability
- **Word count** for each entry
- **Offline support** - works without internet

### 🎨 Terminal Colors

- 🔵 Blue = Headers and sections
- 🟢 Green = Success messages and options
- 🟡 Yellow = Warnings
- 🔴 Red = Errors
- 🟦 Cyan = Information and prompts

### 🔒 Privacy Features

- All entries encrypted before saving
- Local AI processing only
- No network calls (except to localhost:11434 for Ollama)
- Data stored in `~/.privacy_diary/` with restricted permissions
- Encryption key secured with 600 permissions (owner read/write only)

---

## 🔧 Troubleshooting

### "Ollama is not running"

**Solution:**
```bash
# In a separate terminal, start Ollama
ollama serve

# Then try again in the app
```

### "Model not found"

**Solution:**
```bash
# Pull the model
ollama pull llama3

# Or try a different model
ollama pull mistral
```

Then update the script if needed:
```python
DEFAULT_MODEL = "mistral"  # Change this line in the script
```

### Colors not showing properly

**Solution:**
Your terminal might not support ANSI colors. Try:
- Use a modern terminal (iTerm2, Terminal.app on macOS)
- Or disable colors by editing the script (remove Colors.* from print statements)

### Can't type "END" in my entry

**Workaround:**
Just use **Ctrl+D** instead to finish your entry.

---

## 📂 File Locations

All data stored in:
```
~/.privacy_diary/
├── diary_entries.enc  (Your encrypted journal entries)
└── diary.key          (Encryption key - keep safe!)
```

**To view:**
```bash
ls -la ~/.privacy_diary/
```

**To backup:**
```bash
cp -r ~/.privacy_diary ~/Desktop/diary_backup
```

---

## 🎯 Testing Offline

1. Start Ollama: `ollama serve`
2. Run app: `python3 privacy_diary_terminal.py`
3. Write an entry
4. **Turn off WiFi**
5. Request AI analysis
6. ✅ Still works! Everything is local

---

## 📊 Requirements

**Minimal requirements.txt:**
```
cryptography==42.0.5
ollama==0.4.4
```

**Install with:**
```bash
pip install -r requirements.txt
```

---

## 🆘 Quick Commands

```bash
# Start Ollama (separate terminal)
ollama serve

# Run the app
python3 privacy_diary_terminal.py

# Check if Ollama is running
curl http://localhost:11434

# View your entries file (encrypted)
cat ~/.privacy_diary/diary_entries.enc

# Backup your data
cp -r ~/.privacy_diary ~/Desktop/backup-$(date +%Y%m%d)
```

---

## ✨ Pro Tips

1. **Keep Ollama running:** Start it once in a tmux/screen session
2. **Multi-line entries:** Just keep typing, press END when done
3. **Quick saves:** Press Y when prompted (it's the default)
4. **Status check:** Run option 3 if unsure if Ollama is working
5. **Backup regularly:** Copy `~/.privacy_diary` to external drive

---

## 🎉 Enjoy Your Terminal Journal!

Simple, private, and powerful. No GUI needed! ✍️
