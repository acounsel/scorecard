release: python manage.py migrate
web: python manage.py runserver 0.0.0.0:5000
worker: REMAP_SIGTERM=SIGQUIT celery worker --app django_scorecard.celery.app --loglevel info 