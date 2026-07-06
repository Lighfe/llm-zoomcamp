#!/usr/bin/env bash
# setup-secrets.sh — gitignored output, run on Codespace start
set -euo pipefail
b64() { printf '%s' "$1" | base64 -w0; }   # -w0 = no line wrapping

# from github codespace secrets
cat > .env <<EOF
GEMINI_API_KEY=${GEMINI_API_KEY}
SECRET_GEMINI_API_KEY=$(b64 "${GEMINI_API_KEY}")
SECRET_OPENAI_API_KEY=$(b64 "${OPENAI_API_KEY:-}")
SECRET_TAVILY_API_KEY=$(b64 "${TAVILY_API_KEY:-}")
EOF