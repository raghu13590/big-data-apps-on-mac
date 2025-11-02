#!/bin/bash
set -e

# Start Redis and Postgres if needed (for local single-container dev)
if [ "$START_REDIS" = "true" ]; then
  redis-server &
fi
if [ "$START_POSTGRES" = "true" ]; then
  # Start PostgreSQL as the postgres user
  gosu postgres pg_ctlcluster 12 main start
fi

# Superset DB upgrade/init as superset user
gosu superset superset db upgrade

# Create admin user if not exists
gosu superset superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@superset.com \
    --password admin || true

gosu superset superset init
gosu superset which superset
gosu superset superset --version

# Start Superset as superset user
exec gosu superset superset run -p 9088 -h 0.0.0.0