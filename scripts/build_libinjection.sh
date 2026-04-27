#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT_DIR/adiuvare/vendor/libinjection_src"
OUT_DIR="$ROOT_DIR/adiuvare/vendor"

if [[ ! -f "$SRC_DIR/libinjection_sqli.c" || ! -f "$SRC_DIR/libinjection_xss.c" || ! -f "$SRC_DIR/libinjection_html5.c" ]]; then
    echo "libinjection source files are missing from $SRC_DIR" >&2
    exit 1
fi

mkdir -p "$OUT_DIR"

CC_BIN="${CC:-gcc}"
case "$(uname -s)" in
    Darwin)
        OUT_FILE="$OUT_DIR/libinjection.dylib"
        "$CC_BIN" -O2 -fPIC -dynamiclib \
            "$SRC_DIR/libinjection_sqli.c" \
            "$SRC_DIR/libinjection_html5.c" \
            "$SRC_DIR/libinjection_xss.c" \
            -o "$OUT_FILE"
        ;;
    *)
        OUT_FILE="$OUT_DIR/libinjection.so"
        # Linux stays on the plain shared-object path.
        "$CC_BIN" -O2 -fPIC -shared \
            "$SRC_DIR/libinjection_sqli.c" \
            "$SRC_DIR/libinjection_html5.c" \
            "$SRC_DIR/libinjection_xss.c" \
            -o "$OUT_FILE"
        ;;
esac

echo "Built: $OUT_FILE"
