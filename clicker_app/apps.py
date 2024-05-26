from django.apps import AppConfig

class ClickerAppConfig(AppConfig):
    name = 'clicker_app'

    def ready(self):
        import clicker_app.signals
