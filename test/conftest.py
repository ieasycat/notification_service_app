import pytest
from rest_framework.test import APIClient
from main.models import Notification, Client
from datetime import datetime, timedelta


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def create_notification():
    return Notification.objects.create(
        text='test',
        filter='CH',
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1)
    )


@pytest.fixture
def create_client():
    return Client.objects.create(
        phone='+79221119900',
        mobile_code=922,
        tag='CH',
        time_zone="Europe/Moscow"
    )
