from __future__ import absolute_import, unicode_literals
import time
import os

from django.apps import apps

from django_scorecard.celery import app

from .pdf_builder import create_pdf

@app.task
def pdf_creator(ov_id, language, response):
    #allows for the front end to load before displaying stuff
    time.sleep(1)
    Overview = apps.get_model(app_label='scorecard', 
        model_name='Overview')
    overview = Overview.objects.get(id=ov_id)
    return create_pdf(overview, language, response)
    
