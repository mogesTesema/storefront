from time import sleep
from config import celery_app
from celery import shared_task


@shared_task
def notify_customers(message):
    print('Sending 100k emails...')
    print(message)
    sleep(10)
    print('Email were successfully sent!')