import time

from celery import shared_task


@shared_task
def send_sms(phone_number):
    time.sleep(5)
    print(f"SMS отправлено на номер {phone_number}")
