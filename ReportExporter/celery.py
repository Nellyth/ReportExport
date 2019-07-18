from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

name = 'ReportExporter'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings'.format(name))
app = Celery(name)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
