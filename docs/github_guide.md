# GitHub Integration Guide

This document outlines how Version Control was managed for the Smart Expense Tracker.

## Repository Setup
1. **Initialize Git**: 
   ```bash
   git init
   ```
2. **Create `.gitignore`**:
   Ensure `data/`, `__pycache__/`, `.env`, and `*.db` are ignored to prevent uploading sensitive data.

## Commit Strategy
We followed semantic commit messages:
- `feat: added user authentication`
- `fix: resolved database locking issue`
- `docs: updated final year report`
- `style: implemented dark mode UI`
- `refactor: modularized gui components`

## Example Commands
```bash
git add .
git commit -m "feat: complete initial dashboard view"
git branch -M main
git remote add origin https://github.com/username/smart-expense-tracker.git
git push -u origin main
```
