#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit

echo "=========================================="
echo " Building NexCart Backend for Production"
echo "=========================================="

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo ""
echo "Running migrations..."
python manage.py migrate

echo ""
echo "Initializing store settings..."
python manage.py shell -c "from apps.users.models import StoreSettings; StoreSettings.load(); print('Store settings initialized')"

echo ""
echo "=========================================="
echo " Build Complete!"
echo "=========================================="
