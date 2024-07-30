import time
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scripts import views  # Certifique-se de que o caminho para run_sccon está correto
import logging

# Configuração do logger
LOGGER = logging.getLogger('schedules')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

job_instance_sccon = views.JobSccon()

def job_to_sccon():
    LOGGER.info("Iniciando pesquisa de TMS....")
    job_instance_sccon.create_tms()

def list_jobs(scheduler):
    jobs = scheduler.get_jobs()
    for job in jobs:
        print(f"Job id: {job.id}, Next run: {job.next_run_time}, Trigger: {job.trigger}")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_to_sccon, trigger=CronTrigger(day="1", hour=0, minute="0"), id="run_sccon_d1", replace_existing=True)
    scheduler.add_job(job_to_sccon, trigger=CronTrigger(day="8", hour=0, minute="0"), id="run_sccon_d8", replace_existing=True)
    scheduler.add_job(job_to_sccon, trigger=CronTrigger(day="15", hour=0, minute="0"), id="run_sccon_d15", replace_existing=True)
    scheduler.add_job(job_to_sccon, trigger=CronTrigger(day="22", hour=0, minute="0"), id="run_sccon_d22", replace_existing=True)
    scheduler.add_job(job_to_sccon)
    scheduler.start()
    
    LOGGER.info("Start TMS schedules job....")
    print("Scheduler jobs list:")
    list_jobs(scheduler)

    try:
        while True:
            time.sleep(36000)
    except KeyboardInterrupt:
        print("Encerrando o scheduler...")
        scheduler.shutdown()

class Command(BaseCommand):
    """Starts the scheduler to run jobs at specified times""" 

    def handle(self, *args, **kwargs):
        start()
