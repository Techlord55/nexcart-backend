@echo off
REM Windows build script for NexCart Backend
echo ========================================
echo  Building NexCart Backend
echo ========================================

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Collecting static files...
python manage.py collectstatic --no-input

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Initializing store settings...
python -c "from pathlib import Path; from dotenv import load_dotenv; import django; import os; env_path = Path('.env'); load_dotenv(dotenv_path=env_path); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.dev'); django.setup(); from apps.users.models import StoreSettings; StoreSettings.load(); print('Store settings initialized')"

echo.
echo ========================================
echo  Build Complete!
echo ========================================
