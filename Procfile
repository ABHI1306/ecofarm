web: python src/manage.py runserver 0.0.0.0:$PORT
worker: celery -A core worker -l info
celery_beat: celery -A core beat -l info
celerybeatworker: celery -A core worker & celery -A core beat -l INFO & wait -n