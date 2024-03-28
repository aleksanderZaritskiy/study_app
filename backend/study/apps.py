from django.apps import AppConfig


class StudyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "study"

    def ready(self):
        # Импортируйте модуль с сигналами здесь
        import study.signals