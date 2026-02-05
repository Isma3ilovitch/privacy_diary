#!/usr/bin/env python3
"""
The Privacy Diary - Terminal Edition
A 100% Local, Privacy-Preserving Journaling App
Runs entirely in the terminal with local AI analysis using Ollama
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import ollama

# App Configuration
APP_NAME = "The Privacy Diary - Terminal Edition"
DATA_DIR = Path.home() / ".privacy_diary"
ENTRIES_FILE = DATA_DIR / "diary_entries.enc"
KEY_FILE = DATA_DIR / "diary.key"
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)


class Colors:
    """Terminal color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class EncryptionManager:
    """Handles all encryption/decryption operations"""
    
    def __init__(self):
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self):
        """Load existing encryption key or create a new one"""
        if KEY_FILE.exists():
            with open(KEY_FILE, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(KEY_FILE, 'wb') as f:
                f.write(key)
            # Secure the key file (macOS/Linux)
            os.chmod(KEY_FILE, 0o600)
            return key
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt a string and return bytes"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, data: bytes) -> str:
        """Decrypt bytes and return a string"""
        return self.cipher.decrypt(data).decode()


class DiaryStorage:
    """Manages encrypted storage of diary entries"""
    
    def __init__(self, encryption_manager: EncryptionManager):
        self.encryption = encryption_manager
        self.entries = self._load_entries()
    
    def _load_entries(self) -> dict:
        """Load and decrypt all entries from disk"""
        if not ENTRIES_FILE.exists():
            return {}
        
        try:
            with open(ENTRIES_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return {}
            
            decrypted_json = self.encryption.decrypt(encrypted_data)
            return json.loads(decrypted_json)
        except Exception as e:
            print(f"{Colors.RED}Error loading entries: {e}{Colors.END}")
            return {}
    
    def save_entry(self, content: str) -> bool:
        """Save a new entry with timestamp"""
        try:
            timestamp = datetime.now().isoformat()
            self.entries[timestamp] = content
            
            # Encrypt the entire entries dictionary
            json_data = json.dumps(self.entries, indent=2)
            encrypted_data = self.encryption.encrypt(json_data)
            
            # Write encrypted data to disk
            with open(ENTRIES_FILE, 'wb') as f:
                f.write(encrypted_data)
            
            # Secure the entries file
            os.chmod(ENTRIES_FILE, 0o600)
            return True
        except Exception as e:
            print(f"{Colors.RED}Error saving entry: {e}{Colors.END}")
            return False
    
    def get_entry_count(self) -> int:
        """Get total number of entries"""
        return len(self.entries)
    
    def get_recent_entries(self, limit: int = 10) -> list:
        """Get the most recent entries"""
        sorted_entries = sorted(self.entries.items(), reverse=True)
        return sorted_entries[:limit]


class OllamaManager:
    """Manages interaction with local Ollama instance"""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.is_available = False
    
    def check_availability(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Test connection to Ollama
            ollama.list()
            self.is_available = True
            return True
        except Exception as e:
            self.is_available = False
            return False
    
    def analyze_sentiment(self, entry_text: str) -> str:
        """Send entry to local LLM for sentiment analysis"""
        if not self.check_availability():
            return f"{Colors.YELLOW}⚠️  Ollama is not running. Please start Ollama and try again.{Colors.END}"
        
        try:
            prompt = f"""Analyze the sentiment of this journal entry and provide one short, supportive affirmation (2-3 sentences max).

Journal Entry:
{entry_text}

Provide a warm, empathetic response that acknowledges the person's feelings."""

            print(f"{Colors.CYAN}🤔 Analyzing your entry locally...{Colors.END}")
            
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.7,
                    'num_predict': 150  # Keep response concise
                }
            )
            
            return response['message']['content'].strip()
        
        except Exception as e:
            return f"{Colors.RED}⚠️  Analysis failed: {str(e)}\n\nPlease ensure Ollama is running and the '{self.model}' model is installed.{Colors.END}"


def print_banner():
    """Print application banner"""
    print(f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║         🔒  THE PRIVACY DIARY - TERMINAL EDITION        ║
╚══════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}100% Local • Fully Encrypted • Offline AI{Colors.END}
""")


def print_menu():
    """Print main menu"""
    print(f"""
{Colors.BOLD}MAIN MENU:{Colors.END}
  {Colors.GREEN}1.{Colors.END} Write new entry
  {Colors.GREEN}2.{Colors.END} View recent entries
  {Colors.GREEN}3.{Colors.END} Check system status
  {Colors.GREEN}4.{Colors.END} Exit

""")


def write_entry(storage: DiaryStorage, ollama_mgr: OllamaManager):
    """Handle writing a new journal entry"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}═══ NEW JOURNAL ENTRY ═══{Colors.END}\n")
    print(f"{Colors.CYAN}Write your thoughts below. When done, type 'END' on a new line:{Colors.END}\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    
    entry_text = '\n'.join(lines).strip()
    
    if not entry_text:
        print(f"\n{Colors.YELLOW}⚠️  No entry written. Returning to menu.{Colors.END}")
        return
    
    # Show word count
    word_count = len(entry_text.split())
    print(f"\n{Colors.CYAN}📝 Entry written: {word_count} words{Colors.END}")
    
    # Ask if they want AI analysis
    print(f"\n{Colors.BOLD}Would you like AI analysis of this entry?{Colors.END}")
    choice = input(f"{Colors.GREEN}[Y/n]:{Colors.END} ").strip().lower()
    
    if choice != 'n':
        print()
        analysis = ollama_mgr.analyze_sentiment(entry_text)
        print(f"\n{Colors.BOLD}{Colors.BLUE}═══ AI ANALYSIS ═══{Colors.END}\n")
        print(f"{Colors.CYAN}{analysis}{Colors.END}\n")
    
    # Ask if they want to save
    print(f"\n{Colors.BOLD}Save this entry? (will be encrypted with AES-128){Colors.END}")
    choice = input(f"{Colors.GREEN}[Y/n]:{Colors.END} ").strip().lower()
    
    if choice != 'n':
        if storage.save_entry(entry_text):
            print(f"\n{Colors.GREEN}✅ Entry saved successfully!{Colors.END}")
            print(f"{Colors.CYAN}🔒 Encrypted and stored at: {ENTRIES_FILE}{Colors.END}")
            print(f"{Colors.CYAN}📊 Total entries: {storage.get_entry_count()}{Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ Failed to save entry.{Colors.END}")
    else:
        print(f"\n{Colors.YELLOW}Entry discarded.{Colors.END}")


def view_recent_entries(storage: DiaryStorage):
    """Display recent journal entries"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}═══ RECENT ENTRIES ═══{Colors.END}\n")
    
    if storage.get_entry_count() == 0:
        print(f"{Colors.YELLOW}No entries yet. Start writing to see them here!{Colors.END}")
        return
    
    recent = storage.get_recent_entries(limit=5)
    
    for i, (timestamp, content) in enumerate(recent, 1):
        # Parse timestamp
        dt = datetime.fromisoformat(timestamp)
        date_str = dt.strftime("%B %d, %Y at %I:%M %p")
        
        # Preview (first 100 characters)
        preview = content[:100] + "..." if len(content) > 100 else content
        
        print(f"{Colors.BOLD}{i}. {date_str}{Colors.END}")
        print(f"{Colors.CYAN}{preview}{Colors.END}")
        print()
    
    print(f"{Colors.CYAN}📊 Showing {len(recent)} of {storage.get_entry_count()} total entries{Colors.END}")


def check_status(ollama_mgr: OllamaManager, storage: DiaryStorage):
    """Check and display system status"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}═══ SYSTEM STATUS ═══{Colors.END}\n")
    
    # Check Ollama
    ollama_status = ollama_mgr.check_availability()
    
    if ollama_status:
        print(f"{Colors.GREEN}✅ Ollama: Running{Colors.END}")
        print(f"   {Colors.CYAN}Model: {ollama_mgr.model}{Colors.END}")
        print(f"   {Colors.CYAN}Host: localhost:11434{Colors.END}")
    else:
        print(f"{Colors.RED}❌ Ollama: Not Running{Colors.END}")
        print(f"   {Colors.YELLOW}Start with: ollama serve{Colors.END}")
    
    # Storage info
    print(f"\n{Colors.GREEN}✅ Storage: Encrypted{Colors.END}")
    print(f"   {Colors.CYAN}Location: {DATA_DIR}{Colors.END}")
    print(f"   {Colors.CYAN}Entries: {storage.get_entry_count()}{Colors.END}")
    print(f"   {Colors.CYAN}Encryption: AES-128 (Fernet){Colors.END}")
    
    # Privacy status
    print(f"\n{Colors.GREEN}✅ Privacy: Protected{Colors.END}")
    print(f"   {Colors.CYAN}100% Local Processing{Colors.END}")
    print(f"   {Colors.CYAN}No Cloud Connection{Colors.END}")
    print(f"   {Colors.CYAN}No Tracking or Telemetry{Colors.END}")


def main():
    """Main application loop"""
    # Initialize managers
    encryption = EncryptionManager()
    storage = DiaryStorage(encryption)
    ollama = OllamaManager()
    
    # Clear screen and show banner
    os.system('clear' if os.name != 'nt' else 'cls')
    print_banner()
    
    # Main loop
    while True:
        print_menu()
        
        try:
            choice = input(f"{Colors.BOLD}Select option [1-4]:{Colors.END} ").strip()
            
            if choice == '1':
                write_entry(storage, ollama)
            elif choice == '2':
                view_recent_entries(storage)
            elif choice == '3':
                check_status(ollama, storage)
            elif choice == '4':
                print(f"\n{Colors.CYAN}👋 Thank you for using Privacy Diary!{Colors.END}")
                print(f"{Colors.CYAN}Your entries are safe and encrypted.{Colors.END}\n")
                sys.exit(0)
            else:
                print(f"\n{Colors.RED}Invalid option. Please choose 1-4.{Colors.END}")
            
            # Wait for user before showing menu again
            input(f"\n{Colors.BOLD}Press ENTER to continue...{Colors.END}")
            os.system('clear' if os.name != 'nt' else 'cls')
            print_banner()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}👋 Goodbye!{Colors.END}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.END}")


if __name__ == "__main__":
    main()
