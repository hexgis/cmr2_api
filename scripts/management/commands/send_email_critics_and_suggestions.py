from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from scripts.critics_and_suggestions import get_expiration_date
import pytz

class Command(BaseCommand):
    """Starts the scheduler to run jobs at specified times""" 

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler(timezone=pytz.timezone('America/Sao_Paulo'))
        trigger = CronTrigger(hour=9, minute=00)  # Executar todos os dias às 09h00
        scheduler.add_job(get_expiration_date, trigger, id="run_get_expiration_date", replace_existing=True)
        
        scheduler.start()
        self.stdout.write(self.style.SUCCESS('Scheduler started to run get_expiration_date every day at 9AM.'))

        # Manter o processo ativo
        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS('Scheduler stopped.'))
