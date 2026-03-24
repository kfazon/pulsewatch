#!/usr/bin/env sh
set -e

echo "[backend] Starting PulseWatch backend container"

# Optional migration step (best effort). Configure MIGRATION_CMD in compose/.env if needed.
if [ -n "${MIGRATION_CMD:-}" ]; then
  echo "[backend] Running migrations: ${MIGRATION_CMD}"
  sh -c "${MIGRATION_CMD}" || {
    echo "[backend] Migration command failed"
    exit 1
  }
else
  echo "[backend] No MIGRATION_CMD configured; skipping migrations"
fi

# Default long-running backend process. Override with BACKEND_START_CMD when API server exists.
if [ -n "${BACKEND_START_CMD:-}" ]; then
  echo "[backend] Starting app: ${BACKEND_START_CMD}"
  exec sh -c "${BACKEND_START_CMD}"
fi

echo "[backend] No BACKEND_START_CMD configured; using fallback HTTP server on :8000"
exec python -m http.server 8000
