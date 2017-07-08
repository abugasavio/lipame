web: gunicorn config.wsgi:application
worker: celery worker --app=lipame.taskapp --loglevel=info
