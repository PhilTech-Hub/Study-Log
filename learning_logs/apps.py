# apps.py
from django.apps import AppConfig

class LearningLogsConfig(AppConfig):
    name = 'learning_logs'

    def ready(self):
        import learning_logs.signals  # noqa: F401 - This import is necessary to register signals

