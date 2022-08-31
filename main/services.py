from celery.utils.log import get_task_logger
from main.models import Message
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from datetime import datetime
from phonenumber_field.phonenumber import PhoneNumber

logger = get_task_logger(__name__)


def complete_task(task):
    task.enabled = False
    return task.save()


def create_periodic_task(notification_name: datetime, phone: PhoneNumber,
                         id_notification: int, id_client: int, data: dict):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.HOURS,
    )
    return PeriodicTask.objects.create(
        name=f'Create task: {notification_name} for {phone}',
        task='send_notification',
        interval=schedule,
        args=json.dumps([id_notification, id_client, data]),
        start_time=timezone.now(),
    )


def wrong_time_status(message_id: int, start_date: datetime, phone: PhoneNumber,
                      notification_id: int, client_id: int, data: dict):
    logger.info(
        f"Wrong time to send notification '{message_id}'. Need to try later")
    Message.objects.filter(pk=message_id).update(status='Wrong Time')
    create_periodic_task(
        start_date,
        phone,
        notification_id,
        client_id,
        data
    )


def error_status(message_id: int, start_date: datetime, phone: PhoneNumber,
                 notification_id: int, client_id: int, data: dict):
    logger.error(
        f"Notification '{message_id}' is error. Server has problem.")
    Message.objects.filter(pk=message_id).update(status='Error')
    task_error = PeriodicTask.objects.filter(
        name=f'Create task: {start_date}').exists()
    if task_error:
        complete_task(task_error)
    create_periodic_task(
        start_date,
        phone,
        notification_id,
        client_id,
        data
    )


def success_status(message_id: int, start_date: datetime):
    logger.info(f"Notification is '{message_id}' sent success!")
    Message.objects.filter(pk=message_id).update(status='Success')
    task_success = PeriodicTask.objects.filter(
        name=f'Create task: {start_date}').exists()
    if task_success:
        complete_task(task_success)


def waiting_status(message_id: int, start_date: datetime, phone: PhoneNumber,
                   notification_id: int, client_id: int, data: dict):
    Message.objects.filter(pk=message_id).update(status='Waiting')
    create_periodic_task(
        start_date,
        phone,
        notification_id,
        client_id,
        data
    )
