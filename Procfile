web: gunicorn -c gunicorn_config.py app:application
worker: celery -A app.celery worker --loglevel=info
