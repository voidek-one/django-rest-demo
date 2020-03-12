import functools
from django.db.models import signals
from .models import FeedbackModel
from .tasks import send_contact_mail
from django.conf import settings
from django.dispatch import receiver


def suspendingreceiver(signal, **decorator_kwargs):
    def wrapper(func):
        @receiver(signal, **decorator_kwargs)
        @functools.wraps(func)
        def fake_receiver(sender, **kwargs):
            if settings.SUSPEND_SIGNALS:
                return
            return func(sender, **kwargs)
        return fake_receiver
    return wrapper


@suspendingreceiver(signals.post_save, sender=FeedbackModel)
def send_contacts_post_save(sender, instance, signal, *args, **kwargs):
    send_contact_mail.delay(instance.message, instance.email,
                            instance.full_name, instance.files_to_send)
