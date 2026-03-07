#!/bin/bash
set -euo pipefail

# -------------------------------------------------------------
# Bash Automation Script Template
# -------------------------------------------------------------

DRY_RUN=0
INPUT_FILE=""

usage() {
    echo "Usage: $0 [OPTIONS] <input_file>"
    echo "Options:"
    echo "  -h, --help      Display this help message"
    echo "  --dry-run       Run without making changes (enabled by default mostly)"
    exit 1
}

# Parse options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        --dry-run) DRY_RUN=1 ;;
        *)
            if [[ -z "$INPUT_FILE" ]]; then
                INPUT_FILE="$1"
            else
                echo "Unknown parameter passed: $1"; exit 1
            fi
            ;;
    esac
    shift
done

if [[ -z "$INPUT_FILE" ]]; then
    echo "Error: Input file is required."
    usage
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: File not found: $INPUT_FILE"
    exit 1
fi

echo "Starting automation on: $INPUT_FILE"

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY RUN] Would execute destructive operation here."
else
    echo "Executing operation..."
    # COMMAND HERE
fi

echo "Done."
