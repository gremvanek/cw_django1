from django.core.management import BaseCommand
from spam_mailing.tasks import start_scheduler


class Command(BaseCommand):
    help = 'Старт рассылки сообщений...'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки для запуска команды')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        start_scheduler(mailing_id)
