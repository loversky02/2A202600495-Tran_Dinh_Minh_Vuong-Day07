"""
Script to remove emojis from markdown files for professional appearance
"""
import re
from pathlib import Path

# List of markdown files to clean
files_to_clean = [
    "BONUS_FEATURES.md",
    "PROJECT_SUMMARY.md",
    "CHROMADB_TUTORIAL.md",
    "EMBEDDINGS_COMPARISON.md",
    "report/REPORT.md",
]

# Common emojis to remove
emoji_pattern = re.compile(
    "["
    "\U0001F300-\U0001F9FF"  # Emoticons
    "\U00002600-\U000027BF"  # Misc symbols
    "\U0001F680-\U0001F6FF"  # Transport
    "\U00002700-\U000027BF"  # Dingbats
    "\U0001F1E0-\U0001F1FF"  # Flags
    "\u2600-\u26FF"          # Misc symbols
    "\u2700-\u27BF"          # Dingbats
    "\u2B50"                 # Star
    "\u2705"                 # Check mark
    "\u274C"                 # Cross mark
    "\u2714"                 # Heavy check mark
    "\u2716"                 # Heavy X
    "\u2713"                 # Check mark
    "\u2717"                 # X mark
    "]+", 
    flags=re.UNICODE
)

# Additional specific characters to remove
specific_chars = ['✅', '✓', '❌', '✗', '🎯', '🚀', '💡', '📊', '📚', '🔧', 
                  '🎉', '⚡', '💰', '🌐', '🐢', '📝', '🧪', '🎓', '🏆', '📈',
                  '🔍', '📁', '💻', '🔑', '🔄', '💾', '⚠️', '🎁', '💬', '🤔']

def remove_emojis(text):
    """Remove emojis from text"""
    # Remove emoji pattern
    text = emoji_pattern.sub('', text)
    
    # Remove specific characters
    for char in specific_chars:
        text = text.replace(char, '')
    
    # Clean up multiple spaces
    text = re.sub(r'  +', ' ', text)
    
    # Clean up lines that became empty or just whitespace
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # Keep the line if it's not empty or if it's part of formatting
        if stripped or (not stripped and cleaned_lines and cleaned_lines[-1].strip()):
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def clean_file(filepath):
    """Clean a single file"""
    path = Path(filepath)
    if not path.exists():
        print(f"  Skipping {filepath} (not found)")
        return False
    
    print(f"  Cleaning {filepath}...")
    
    # Read file
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove emojis
    cleaned = remove_emojis(content)
    
    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    # Count changes
    original_len = len(content)
    cleaned_len = len(cleaned)
    removed = original_len - cleaned_len
    
    print(f"    Removed {removed} characters")
    return True

def main():
    print("=" * 80)
    print("REMOVING EMOJIS FROM MARKDOWN FILES")
    print("=" * 80)
    print("\nThis will make documentation more professional and less AI-generated looking.")
    print()
    
    cleaned_count = 0
    for filepath in files_to_clean:
        if clean_file(filepath):
            cleaned_count += 1
    
    print()
    print("=" * 80)
    print(f"COMPLETED: Cleaned {cleaned_count}/{len(files_to_clean)} files")
    print("=" * 80)
    print("\nFiles are now more professional without emojis.")
    print("Review the changes with: git diff")

if __name__ == "__main__":
    main()
