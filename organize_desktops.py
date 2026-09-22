import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
TARGET_DIRS = [
    Path(r"C:\Users\alberto.tummillo\Desktop"),
    Path(r"C:\Users\alberto.tummillo\OneDrive - COMEF SRL\Desktop")
]

# Mapping of folder names to the keywords or extensions they should contain
RULES = {
    "Reports": {
        "extensions": [".pdf", ".docx"],
        "keywords": ["documenti", "verbale", "report", "rotocella", "strumentazione"]
    },
    "RdO_Automation": {
        "extensions": [".py", ".txt", ".png"],
        "keywords": ["prmRdO", "forniture", "logo"]
    },
    "PM_Resources": {
        "extensions": [".xlsx", ".xls"],
        "keywords": ["WBS", "budget", "confrontoWbs", "CET", "Ore"]
    },
    "AI_Learning": {
        "extensions": [".md", ".html"],
        "keywords": ["llm", "prompt", "AGI", "Claude"]
    },
    "Shortcuts_and_Links": {
        "extensions": [".lnk", ".rdp"],
        "keywords": []
    }
}

def organize_folder(base_path):
    if not base_path.exists():
        print(f"Skipping: {base_path} (not found)")
        return

    print(f"Organizing: {base_path}")
    
    # Create subdirectories if they don't exist
    for folder in RULES.keys():
        (base_path / folder).mkdir(exist_ok=True)

    # Iterate over files in the root of the desktop
    for item in base_path.iterdir():
        if item.is_file():
            # Skip hidden files or files starting with .
            if item.name.startswith(".") or item.name == "desktop.ini":
                continue
                
            moved = False
            for folder, criteria in RULES.items():
                ext_match = item.suffix.lower() in criteria["extensions"]
                kw_match = any(kw.lower() in item.name.lower() for kw in criteria["keywords"])
                
                if ext_match or kw_match:
                    dest = base_path / folder / item.name
                    print(f"  Moving {item.name} -> {folder}/")
                    try:
                        shutil.move(str(item), str(dest))
                        moved = True
                        break
                    except Exception as e:
                        print(f"    Error moving {item.name}: {e}")
            
            if not moved:
                print(f"  Uncategorized: {item.name}")

if __name__ == "__main__":
    for path in TARGET_DIRS:
        organize_folder(path)
    print("Organization complete.")
