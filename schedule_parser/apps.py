from django.apps import AppConfig
import os
from schedule_parser import parser
from apscheduler.schedulers.background import BackgroundScheduler


class ScheduleParserConfig(AppConfig):
    name = 'schedule_parser'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            # parser.parse()
            scheduler = BackgroundScheduler()
            scheduler.add_job(parser.parse, trigger='cron', hour='19', minute='00')
            scheduler.add_job(parser.parse, trigger='cron', hour='00', minute='00')
            scheduler.start()
