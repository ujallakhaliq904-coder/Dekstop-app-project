# Deployment Guide

This application can be packaged into a standalone Windows executable using PyInstaller.

## Prerequisites
Ensure PyInstaller is installed:
```bash
pip install pyinstaller
```

## Build Process
Run the following command in the project root:
```bash
pyinstaller --onefile --windowed --name "SmartExpenseTracker" main.py
```

- `--onefile`: Bundles everything into a single `.exe`.
- `--windowed`: Prevents the command prompt console from appearing when the GUI runs.

## Output
The final executable will be located in the `dist/` directory:
`dist/SmartExpenseTracker.exe`

## Distribution
Simply share the `.exe` file. The application will automatically create the `data/` folder and `expenses.db` database in the directory where the executable is run.
