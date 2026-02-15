from django.apps import AppConfig


class ServiceDeskConfig(AppConfig):
    name = 'service_desk'

    def ready(self):
        import service_desk.signals
