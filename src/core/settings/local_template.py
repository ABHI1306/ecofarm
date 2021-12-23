SECRET_KEY = ''

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eco',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'PORT': '5432',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""  
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_ADDRESS = ''
DEFAULT_EMAIL_FROM = ''

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
