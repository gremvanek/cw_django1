from django.apps import AppConfig


class SpamMailingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spam_mailing"

    def ready(self):
        import time
        from spam_mailing.models import Mailing
        from spam_mailing.tasks import start_scheduler, schedulers
        mailings = Mailing.objects.filter(status='started')
        print("Начинаю рассылку...")
        for mailing in mailings:
            if mailing.id not in schedulers:
                start_scheduler(mailing.id)
            time.sleep(3)  # Для демонстрации, чтобы не было слишком быстро
