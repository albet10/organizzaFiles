import os
import shutil
import traceback
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# --- CONFIGURATION ---
TARGET_DIRS = [
    Path(r"C:\Users\alberto.tummillo\Desktop"),
    Path(r"C:\Users\alberto.tummillo\OneDrive - COMEF SRL\Desktop")
]

# File di log: viene creato nella stessa cartella dello script e
# ogni esecuzione viene AGGIUNTA in coda (non sovrascrive le precedenti)
LOG_FILE = Path(__file__).resolve().parent / "desktop_organization_log.txt"

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


def build_ascii_tree(base_path, moved_files, uncategorized_files):
    """
    Costruisce le righe di un albero ASCII per una cartella desktop:
    - moved_files: dict {nome_sottocartella: [nomi_file spostati]}
    - uncategorized_files: [nomi_file non spostati]
    """
    lines = [str(base_path)]

    entries = [(folder, files) for folder, files in moved_files.items() if files]
    if uncategorized_files:
        entries.append(("Non categorizzati (non spostati)", uncategorized_files))

    if not entries:
        lines.append("└── (nessun file spostato)")
        return lines

    for i, (folder, files) in enumerate(entries):
        is_last_folder = (i == len(entries) - 1)
        folder_connector = "└── " if is_last_folder else "├── "
        lines.append(f"{folder_connector}{folder}")
        prefix = "    " if is_last_folder else "│   "
        for j, fname in enumerate(files):
            is_last_file = (j == len(files) - 1)
            file_connector = "└── " if is_last_file else "├── "
            lines.append(f"{prefix}{file_connector}{fname}")

    return lines


def organize_folder(base_path, log_lines):
    """
    Organizza una cartella desktop e aggiunge il risultato (albero ASCII)
    a log_lines. Restituisce la lista di eventuali errori incontrati.
    """
    moved_files = defaultdict(list)
    uncategorized_files = []
    errors = []

    if not base_path.exists():
        print(f"Skipping: {base_path} (not found)")
        log_lines.append(str(base_path))
        log_lines.append("└── (cartella non trovata)")
        return errors

    print(f"Organizing: {base_path}")

    # Create subdirectories if they don't exist
    for folder in RULES.keys():
        try:
            (base_path / folder).mkdir(exist_ok=True)
        except Exception as e:
            errors.append(f"Errore creando la cartella '{folder}': {e}")

    # Iterate over files in the root of the desktop (ordine alfabetico per un log leggibile)
    for item in sorted(base_path.iterdir(), key=lambda p: p.name.lower()):
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
                        moved_files[folder].append(item.name)
                        moved = True
                        break
                    except Exception as e:
                        error_msg = f"Errore spostando '{item.name}' in '{folder}': {e}"
                        print(f"    {error_msg}")
                        errors.append(error_msg)

            if not moved:
                uncategorized_files.append(item.name)
                print(f"  Uncategorized: {item.name}")

    log_lines.extend(build_ascii_tree(base_path, moved_files, uncategorized_files))
    return errors


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines = []
    all_errors = []

    try:
        for path in TARGET_DIRS:
            try:
                errors = organize_folder(path, log_lines)
                all_errors.extend(errors)
            except Exception as e:
                err_msg = f"Errore critico processando '{path}': {e}"
                all_errors.append(err_msg)
                log_lines.append(str(path))
                log_lines.append(f"└── (errore critico: {e})")
            log_lines.append("")  # riga vuota tra una cartella e l'altra

        status = "SUCCESSO" if not all_errors else "COMPLETATO CON ERRORI"

    except Exception:
        status = "FALLITO"
        all_errors.append("Errore critico non gestito durante l'esecuzione")
        log_lines.append(traceback.format_exc())

    header = [
        "=" * 80,
        f"Esecuzione: {timestamp}",
        f"Stato: {status}",
        "-" * 80,
    ]
    if all_errors:
        header.append("Errori riscontrati:")
        for err in all_errors:
            header.append(f"  - {err}")
        header.append("-" * 80)

    full_entry = header + log_lines + ["=" * 80, ""]

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(full_entry) + "\n")
        print(f"\nLog scritto in: {LOG_FILE}")
    except Exception as e:
        print(f"\nImpossibile scrivere il file di log ({LOG_FILE}): {e}")

    print("Organization complete." if status == "SUCCESSO" else f"Organization finished with status: {status}")


if __name__ == "__main__":
    main()
