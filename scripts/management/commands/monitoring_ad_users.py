from typing import Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scripts import views
from django.core.management.base import BaseCommand
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

instance = views.JobMonitoringAd()

def job_to_monitoring_ad_users():
    instance.sincronize_with_django()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_to_monitoring_ad_users, trigger='interval', hours=24)
    scheduler.add_job(job_to_monitoring_ad_users)
    scheduler.start()
    logger.debug("Scheduler started and job added to update users from FUNAI AD.")

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        start()
