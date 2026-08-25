#!/usr/bin/env bash
# Port agent-chat sidebar state from the old Football-TDA workspace to ~/TDA/Football.
#
# Chat bodies live in Cursor's global database and are keyed by UUID — they survive
# a folder move. What breaks is the workspace link: which chats appear in the
# Agents sidebar for this folder. This script copies those keys across.
#
# Run ONCE, with Cursor fully quit:
#   bash 08_current/scripts/migrate_cursor_workspace.sh
#
# Prerequisite: you have opened ~/TDA/Football in Cursor at least once so the new
# workspace storage folder exists.

set -euo pipefail

OLD_WS=3f13f85daa30ca264d70d7c37c62e635   # Documents/GitHub/Football-TDA
NEW_FOLDER='file:///Users/rowanbrown/TDA/Football'
WS_ROOT="$HOME/Library/Application Support/Cursor/User/workspaceStorage"

OLD_DB="$WS_ROOT/$OLD_WS/state.vscdb"

if pgrep -xq Cursor || pgrep -xq 'Cursor Helper'; then
  echo "ERROR: Quit Cursor completely before running this script."
  exit 1
fi

if [[ ! -f "$OLD_DB" ]]; then
  echo "ERROR: Old workspace database not found at $OLD_DB"
  exit 1
fi

NEW_WS=
for d in "$WS_ROOT"/*/workspace.json; do
  if grep -q 'TDA/Football' "$d" 2>/dev/null; then
    NEW_WS=$(basename "$(dirname "$d")")
    break
  fi
done

if [[ -z "$NEW_WS" ]]; then
  echo "ERROR: No workspace storage found for $NEW_FOLDER."
  echo "Open ~/TDA/Football in Cursor once (File → Open Folder), quit Cursor, then re-run."
  exit 1
fi

NEW_DB="$WS_ROOT/$NEW_WS/state.vscdb"
echo "Old workspace: $OLD_WS"
echo "New workspace: $NEW_WS"

python3 - <<PY
import sqlite3
from pathlib import Path

old_db = Path("$OLD_DB")
new_db = Path("$NEW_DB")

prefixes = (
    "composer.",
    "workbench.backgroundComposer.",
    "workbench.panel.composerChatViewPane.",
    "workbench.panel.aichat.",
    "agentSidebar.",
    "agentLayout",
    "newAgentSidebar.",
    "ideSidebar.section.agents",
)

old = sqlite3.connect(old_db)
new = sqlite3.connect(new_db)
copied = 0
for key, value in old.execute("SELECT key, value FROM ItemTable"):
    if key.startswith(prefixes):
        new.execute(
            "INSERT INTO ItemTable(key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )
        copied += 1
new.commit()
old.close()
new.close()
print(f"Copied {copied} workspace keys into {new_db.name}")
PY

echo
echo "Done. Reopen Cursor at ~/TDA/Football — your agent chats should appear in the sidebar."
echo "Project transcripts are already at ~/.cursor/projects/Users-rowanbrown-TDA-Football/"
