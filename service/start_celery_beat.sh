#!/bin/bash
celery -A service beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler