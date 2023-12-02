from django.core.mail import send_mail
from django.conf import settings


def send_email(text: str, receiver: str):
    subject = 'Это тема письма!'
    message = text
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [receiver, ])
