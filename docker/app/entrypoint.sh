#!/usr/bin/env bash

# wait for database container to accept connections, because:
# - docker compose service_healthy condition causes docker compose run to fail
# - it's useful for isolated container runs without docker compose dependency management
wait-for-it \
  --host="${TINYURL2_DATABASE_HOST}" \
  --port="${TINYURL2_DATABASE_PORT:-5432}" \
  --timeout=30 \
  --strict

exec "$@"
