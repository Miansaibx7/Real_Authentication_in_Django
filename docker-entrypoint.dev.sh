#!/bin/sh

# Responsibilities:
#   Stop immediately if a command fails.
#   Check the Django project configuration.
#   Apply database migrations.
#   Collect static files when required.
#   Start Django's development server.

# Django settings:
#   config.settings
#
# Development server:
#   0.0.0.0:8000


set -e

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

PROJECT_DIR="/app/config"
MANAGE_PY="${PROJECT_DIR}/manage.py"
HOST="${DJANGO_HOST:-0.0.0.0}"
PORT="${DJANGO_PORT:-8000}"

echo ""
echo "============================================================"
echo "  Real Authentication in Django"
echo "  Development Container"
echo "============================================================"
echo ""

# ------------------------------------------------------------
# 1. Check Python
# ------------------------------------------------------------

echo ">>> Checking Python..."

python --version

# ------------------------------------------------------------
# 2. Check Django
# ------------------------------------------------------------

echo ""
echo ">>> Checking Django..."

python -m django --version

# ------------------------------------------------------------
# 3. Verify the Django project exists
# ------------------------------------------------------------

echo ""
echo ">>> Checking Django project..."

if [ ! -f "$MANAGE_PY" ]; then
    echo "ERROR: Django manage.py was not found:"
    echo "       $MANAGE_PY"
    exit 1
fi

echo "Django project found:"
echo "  $MANAGE_PY"

# ------------------------------------------------------------
# 4. Run Django system checks
# ------------------------------------------------------------

echo ""
echo ">>> Running Django system checks..."

python "$MANAGE_PY" check

# ------------------------------------------------------------
# 5. Apply database migrations
# ------------------------------------------------------------
#
# This applies migrations that have not yet been applied.
#
# It is safe for normal development because:
#
#     migrate
#
# does NOT delete existing data.
#
# IMPORTANT:
# Do NOT use:
#
#     migrate --fake
#     migrate --run-syncdb
#     migrate --fake-initial
#
# automatically here unless your project specifically requires
# them.
# ------------------------------------------------------------

echo ""
echo ">>> Applying database migrations..."

python "$MANAGE_PY" migrate --noinput

# ------------------------------------------------------------
# 6. Collect static files
# ------------------------------------------------------------
#
# This is useful when STATIC_ROOT is configured.
#
# If your development configuration does not require static
# collection, you can disable it with:
#
#     COLLECT_STATIC=false
#
# ------------------------------------------------------------

if [ "${COLLECT_STATIC:-true}" = "true" ]; then

    echo ""
    echo ">>> Collecting static files..."

    python "$MANAGE_PY" collectstatic --noinput

else

    echo ""
    echo ">>> Skipping collectstatic..."

fi

# ------------------------------------------------------------
# 7. Final Django system check
# ------------------------------------------------------------

echo ""
echo ">>> Performing final Django check..."

python "$MANAGE_PY" check

# ------------------------------------------------------------
# 8. Start Django development server
# ------------------------------------------------------------

echo ""
echo "============================================================"
echo "  Django development server is starting"
echo "============================================================"
echo ""
echo "  Host : $HOST"
echo "  Port : $PORT"
echo "  URL  : http://localhost:$PORT"
echo ""
echo "  Admin:"
echo "  http://localhost:$PORT/admin/"
echo ""
echo "  API:"
echo "  http://localhost:$PORT/api/auth/"
echo ""
echo "============================================================"
echo ""

# exec replaces the shell process with Django.
#
# This is important for Docker because Django receives
# termination signals directly and Docker can stop/restart
# the container cleanly.

exec python "$MANAGE_PY" runserver "${HOST}:${PORT}"