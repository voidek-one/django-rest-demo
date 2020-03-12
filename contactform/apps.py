from django.apps import AppConfig


class ContactformConfig(AppConfig):
    name = 'contactform'

    def ready(self):
        import contactform.signals
