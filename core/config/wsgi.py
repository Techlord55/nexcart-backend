# Location: core\config\wsgi.py
"""
WSGI config for NexCart project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings.prod')

application = get_wsgi_application()
