from celery.app import shared_task
from django.core.mail import send_mail
from cryptography.fernet import Fernet
import time

key = Fernet.generate_key()
fernet = Fernet(key)

def send_activation_email(new_user, email, sub_, msg_):
    encoding = 'utf-8'
    token_ = str(fernet.encrypt_at_time((str(new_user.id) +"%"+sub_).encode(),current_time=int(time.time())), encoding)
    subject = sub_
    email_from = 'abhijitshete13@gmail.com'
    recipient_list = [email]
    message = f'{msg_}{token_}'
    send_mail(subject, message, email_from, recipient_list)
        
def verify_email_by_token(tk):
    """ Getting token from request if token is valid then email verification is done otherwise verification is not done. """
    user_id = fernet.decrypt_at_time(tk,ttl=3600,current_time=int(time.time())).decode()
    return user_id
    
           