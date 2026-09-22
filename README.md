# Desktop Organization Automation (v0.2)

This folder contains a Python script designed to automatically declutter and organize your local and OneDrive Desktop folders — with an execution log.

## Files
- `organize_desktops_0.2.py`: The main automation script.
- `README_Desktop_Organization_0.2.md`: This instruction file.
- `desktop_organization_log.txt`: Created automatically next to the script on first run.

## How the Script Works
The script scans the root of your Desktop folders and moves files into subdirectories based on predefined rules:
- **Reports**: Moves `.pdf` and `.docx` files or files containing keywords like "report" or "verbale".
- **RdO_Automation**: Moves `.py`, `.txt`, and `.png` files related to your automation tools.
- **PM_Resources**: Moves `.xlsx` and `.xls` files related to project management (WBS, budgets, etc.).
- **AI_Learning**: Moves `.md` and `.html` files related to AI research and LLMs.
- **Shortcuts_and_Links**: Moves all `.lnk` (shortcuts) and `.rdp` (remote desktop) files.

## What's new in v0.2 — Execution Log
Every run appends an entry to `desktop_organization_log.txt` (same folder as the script) containing:
1. **Execution date/time**
2. **Status**: `SUCCESSO`, `COMPLETATO CON ERRORI`, or `FALLITO`, plus a list of any errors encountered
3. **ASCII tree** of where each file was moved, per Desktop folder

Example entry:
```
================================================================================
Esecuzione: 2026-09-22 14:35:10
Stato: SUCCESSO
--------------------------------------------------------------------------------
C:\Users\alberto.tummillo\Desktop
├── Reports
│   ├── verbale_riunione_23set.pdf
│   └── report_ottobre.docx
├── PM_Resources
│   └── budget_2026.xlsx
└── Non categorizzati (non spostati)
    └── appunti_vari.txt

C:\Users\alberto.tummillo\OneDrive - COMEF SRL\Desktop
└── (nessun file spostato)
================================================================================
```
The log file is never overwritten — each execution is appended, so you get a running history of every cleanup.

## Customizing Rules
To change where files go, open `organize_desktops_0.2.py` in a text editor and modify the `RULES` dictionary:
```python
RULES = {
    "FolderName": {
        "extensions": [".ext1", ".ext2"],
        "keywords": ["word1", "word2"]
    },
    ...
}
```

## How to Schedule (Windows Task Scheduler)
To run this cleanup automatically every month:

1.  **Open Task Scheduler**: Press `Win + R`, type `taskschd.msc`, and hit Enter.
2.  **Create Task**: Click `Create Basic Task...` in the Actions panel.
3.  **Name**: Set to `Monthly Desktop Cleanup`.
4.  **Trigger**: Select `Monthly`. Pick a day (e.g., the 1st) and a time.
5.  **Action**: Select `Start a Program`.
6.  **Settings**:
    - **Program/script**: `pythonw.exe` (runs silently, no console window — recommended for a scheduled task)
    - **Add arguments**: `"C:\Users\alberto.tummillo\Desktop\organize_desktops_0.2.py"`
7.  **Finish**: The script will now run silently in the background once a month, and every run will be recorded in `desktop_organization_log.txt`.

> Tip: since `pythonw.exe` shows no window, the log file is the only way to check whether a scheduled run succeeded — open it after each scheduled date to confirm the status and see what moved.

## Manual Run
Run `python organize_desktops_0.2.py` from a command prompt (recommended, so you see the console output too), or double-click the file to trigger the organization immediately. Either way, the run is also recorded in the log.
