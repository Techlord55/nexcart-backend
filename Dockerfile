# NexCart Backend Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
# Added 'curl' for healthchecks and cleaned up apt cache in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories and set permissions
# It's better to create a non-privileged user for production security
RUN mkdir -p logs ml_models staticfiles media && \
    adduser --disabled-password --no-create-home nexuser && \
    chown -R nexuser:nexuser /app

# Switch to the non-root user
USER nexuser

# Expose port
EXPOSE 8000

# The CMD should use the shell form to allow environment variable expansion
# Use 3 workers as you planned - good for small/medium production servers
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn core.config.wsgi:application --bind 0.0.0.0:8000 --workers 3