#!/usr/bin/env bash
set -euo pipefail

# Root = directory containing this script (Algo Coding)
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_DEST="$ROOT/All/Python files"
CPP_DEST="$ROOT/All/C++ files"

mkdir -p "$PY_DEST" "$CPP_DEST"

# Flatten relative path to a unique filename (slashes -> __)
flatten_name() {
  local rel="$1"
  echo "${rel//\//__}"
}

while IFS= read -r -d '' f; do
  rel="${f#"$ROOT"/}"
  base="$(flatten_name "$rel")"
  case "$f" in
    *.py)  cp -f "$f" "$PY_DEST/$base" ;;
    *.cpp) cp -f "$f" "$CPP_DEST/$base" ;;
  esac
done < <(find "$ROOT" -path "$ROOT/All" -prune -o -type f \( -name "*.py" -o -name "*.cpp" \) -print0)

echo "Done. Python -> $PY_DEST"
echo "Done. C++    -> $CPP_DEST"
