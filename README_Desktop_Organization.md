# Desktop Organization Automation

This folder contains a Python script designed to automatically declutter and organize your local and OneDrive Desktop folders.

## Files
- `organize_desktops.py`: The main automation script.
- `README_Desktop_Organization.md`: This instruction file.

## How the Script Works
The script scans the root of your Desktop folders and moves files into subdirectories based on predefined rules:
- **Reports**: Moves `.pdf` and `.docx` files or files containing keywords like "report" or "verbale".
- **RdO_Automation**: Moves `.py`, `.txt`, and `.png` files related to your automation tools.
- **PM_Resources**: Moves `.xlsx` and `.xls` files related to project management (WBS, budgets, etc.).
- **AI_Learning**: Moves `.md` and `.html` files related to AI research and LLMs.
- **Shortcuts_and_Links**: Moves all `.lnk` (shortcuts) and `.rdp` (remote desktop) files.

## Customizing Rules
To change where files go, open `organize_desktops.py` in a text editor and modify the `RULES` dictionary:
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
    - **Program/script**: `pythonw.exe`
    - **Add arguments**: `"C:\Users\alberto.tummillo\Desktop\organize_desktops.py"`
7.  **Finish**: The script will now run silently in the background once a month.

## Manual Run
Simply double-click `organize_desktops.py` to trigger the organization immediately.
