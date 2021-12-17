web: python src/manage.py runserver 0.0.0.0:$PORT
worker: celery --workdir src -A core worker -l info
celery_beat: celery --workdir src -A  core beat -l info
celerybeatworker: celery --workdir src -A core worker & --workdir src celery -A core beat -l INFO & wait -n