import requests
import pytz
import datetime
from main.services import wrong_time_status, error_status, success_status, waiting_status
from notification_service.celery import app
from main.models import Notification, Client
from config import CONFIG


@app.task(bind=True, retry_backoff=5)
def send_notification(self, notification_id: int, client_id: int, data, url=CONFIG.URL, token=CONFIG.TOKEN):
    notification = Notification.objects.get(pk=notification_id)
    client = Client.objects.get(pk=client_id)
    timezone_client = pytz.timezone(client.time_zone)
    datetime_client = datetime.datetime.now(timezone_client)

    if notification.start_date <= datetime_client <= notification.end_date:
        if 22 < datetime_client.hour or datetime_client.hour < 8:
            wrong_time_status(
                message_id=data['id'],
                phone=client.phone,
                start_date=notification.start_date,
                notification_id=notification.id,
                client_id=client.id,
                data=data
            )

        else:
            header = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'}
            try:
                requests.post(
                    url=url + str(data['id']), headers=header, json=data)
            except requests.exceptions.RequestException as exc:
                error_status(
                    message_id=data['id'],
                    start_date=notification.start_date,
                    phone=client.phone,
                    notification_id=notification.id,
                    client_id=client.id,
                    data=data
                )
                raise exc
            else:
                success_status(
                    message_id=data['id'],
                    start_date=notification.start_date,
                )

    elif datetime_client < notification.start_date:
        waiting_status(
            message_id=data['id'],
            start_date=notification.start_date,
            phone=client.phone,
            notification_id=notification.id,
            client_id=client.id,
            data=data
        )
