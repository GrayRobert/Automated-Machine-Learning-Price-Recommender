#!/bin/bash
# Activate virtual environment
. /venv/bin/activate

# Download requirements to build cache
pip3 download -d /build -r requirements.txt --no-input

# Install application requirements
pip3 install --no-index -f /build -r requirements.txt

# Download production requirements to build cache
pip3 download -d /build -r requirements.production.txt --no-input

# Install production application requirements
pip3 install --no-index -f /build -r requirements.production.txt

# Install AUTO-SKLEARN & TPOT
pip3 install auto-sklearn tpot

# Run main.py
python /app/manage.py makemigrations && python /app/manage.py migrate && python /app/manage.py runserver 0.0.0.0:8000

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'grayarobert@gmail.com', 'admin123$')" | ./manage.py shell