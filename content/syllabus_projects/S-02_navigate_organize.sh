#!/bin/bash
# S-02 — Navigate & Organize Your Own Project Folders
# Practices cd, ls, mkdir, mv in a throwaway sandbox folder so it's safe to
# run and re-run without touching any real project files.

set -e

SANDBOX="$(mktemp -d)"
cd "$SANDBOX"
echo "Working in sandbox: $SANDBOX"

echo "hello from a test file" > file.txt

echo ""
echo "--- ls (list files here) ---"
ls

echo ""
echo "--- mkdir NewFolder (make a new folder) ---"
mkdir NewFolder
ls

echo ""
echo "--- mv file.txt NewFolder (move the file into it) ---"
mv file.txt NewFolder
ls NewFolder

echo ""
echo "Done. Cleaning up sandbox."
rm -rf "$SANDBOX"
