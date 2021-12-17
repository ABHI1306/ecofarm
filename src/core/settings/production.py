import os
import dj_database_url
import psycopg2

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-5t-*z-!yo)2x-b=qq223555$2=)#5m%0$_4((05j_gga38pa5&")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'true').lower() == "true"

#CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

#DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get(os.environ.get("DATABASE_URL_CONFIG")))
DEFAULT_CONNECTION = dj_database_url.parse(os.environ.get("DATABASE_URL"))

conn=psycopg2.connect(
  database="eco",
  user="postgres",
  host="/tmp/",
  password="postgres",
  port="5432",
)

DEFAULT_CONNECTION.update({"CONN_MAX_AGE": 600})
DATABASES = {"default": DEFAULT_CONNECTION}
ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS',[])
CELERY_BROKER_URL = os.environ.get('REDIS_URL') 
