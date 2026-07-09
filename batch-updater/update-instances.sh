#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="$SCRIPT_DIR/instances.conf"
HELPER="$SCRIPT_DIR/update-helper.cjs"
DEFAULT_TEMPLATE="$SCRIPT_DIR/../scribboleth.html"
TEMPLATE="${1:-$DEFAULT_TEMPLATE}"

if [ ! -f "$CONF" ]; then
    echo "instances.conf not found at $CONF"
    exit 1
fi

if [ ! -f "$HELPER" ]; then
    echo "update-helper.cjs not found at $HELPER"
    exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
    echo "Template not found at $TEMPLATE"
    exit 1
fi

if ! command -v node &>/dev/null; then
    echo "Node.js is required but not found in PATH"
    exit 1
fi

count=0
while IFS= read -r line || [ -n "$line" ]; do
    line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [ -z "$line" ] && continue

    if [ ! -f "$line" ]; then
        echo "[SKIP] File not found: $line"
        continue
    fi

    echo "[INSTANCE] $line"
    node "$HELPER" "$line" "$TEMPLATE"

    count=$((count + 1))
done < "$CONF"

echo ""
echo "Done. $count instance(s) processed."
