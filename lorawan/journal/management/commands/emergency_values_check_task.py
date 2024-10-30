import journal.service
import web_app.service
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = 'Выполнение периодической задачи'

    def handle(self, *args, **kwargs):
        data = web_app.service.get_data_from_all_devices()
        messages = journal.service.compare_data_and_emergency_settings(data)
        journal.service.create_journal_sign(messages)
        now = datetime.now()
        self.stdout.write(f"Периодическая задача выполнена в {now}")
