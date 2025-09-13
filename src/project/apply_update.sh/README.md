# apply_update.sh Utility

## Overview
Applies zipped updates to local AkashaOS repo. Handles:
- Unpacking updates
- Removing nested `.git` folders
- Staging, committing, and pushing changes
- Preserving files safely

## Usage
```bash
./apply_update.sh <path-to-zip>
```

Example:
```bash
./apply_update.sh ~/Downloads/autopilot_update.zip
```

## Workflow
1. Checks zip file path
2. Unzips into `$HOME/AkashaOS`
3. Removes nested `.git`
4. Stages all changes
5. Commits and pushes

## Safety
- Verify `$HOME/AkashaOS` points to intended repo
- Backup if needed
