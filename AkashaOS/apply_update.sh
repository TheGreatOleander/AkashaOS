#!/bin/bash
set -e

TARGET="$HOME/AkashaOS"
ZIPFILE="$1"

if [ -z "$ZIPFILE" ]; then
  echo "Usage: $0 <path-to-zip>"
  exit 1
fi

echo "Applying update from $ZIPFILE to $TARGET..."

# Unzip update into repo (overwrite existing files)
unzip -o "$ZIPFILE" -d "$TARGET"

cd "$TARGET"

# Remove any nested .git dirs
find "$TARGET/resources" -type d -name ".git" -exec rm -rf {} +

# Stage, commit, push
git add .
git commit -m "Apply automated update from $ZIPFILE"
git push origin main

echo "✅ Update applied and pushed."
