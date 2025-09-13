#!/usr/bin/env bash
set -euo pipefail

# cleanup_backups.sh - move backup/update artifacts into a dated folder and commit

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DEST_DIR="cleanup_backups/${TIMESTAMP}"
mkdir -p "$DEST_DIR"

# patterns to clean
patterns=( '*.bak' '*.orig*' '*~' '*.swp' '*.tmp' '*.old' )

echo "Searching for backup/update artifact patterns..."
found=0
for p in "${patterns[@]}"; do
  while IFS= read -r -d '' file; do
    # skip files inside .git or the cleanup dir itself
    if [[ "$file" == .git* ]] || [[ "$file" == "$DEST_DIR/"* ]]; then
      continue
    fi
    mkdir -p "$(dirname "$DEST_DIR/$file")"
    mv -- "$file" "$DEST_DIR/$file"
    echo "Moved: $file -> $DEST_DIR/$file"
    found=$((found+1))
  done < <(find . -type f -name "$p" -print0)
done

if [[ $found -eq 0 ]]; then
  echo "No backup/update artifacts found."
  exit 0
fi

echo "Staging moved files..."
git add -A
git commit -m "chore: cleanup backup/update artifacts moved to ${DEST_DIR}"
echo "Cleanup complete. ${found} files moved to ${DEST_DIR} and committed."

echo "Tip: if you want to restore any moved file, it's now in the repo at $DEST_DIR (and in Git history)."
