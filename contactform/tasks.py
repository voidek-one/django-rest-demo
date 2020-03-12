from __future__ import absolute_import, unicode_literals
from settings.celery import app
from .utils import send_email


@app.task
def send_contact_mail(message, email, full_name, files_to_send):
    send_email(message, email, full_name, files_to_send)
