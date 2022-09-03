import pytest
import json
from main.models import Notification, Client
from datetime import datetime, timedelta


@pytest.mark.django_db
def test_get_clients(client_api, create_client):
    response = client_api.get('/api/v1/client/', content_type='application/json')
    data = dict(response.data['results'][0])

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert data == {
        'id': 1,
        'phone': '+79221119900',
        'mobile_code': '922',
        'tag': 'CH',
        'time_zone': 'Europe/Moscow'
    }


@pytest.mark.django_db
def test_create_client(client_api):
    data = {
        'phone': '+79221189900',
        'mobile_code': '922',
        'tag': "WR",
        'time_zone': "Europe/Moscow"
    }
    response = client_api.post('/api/v1/client/', data=json.dumps(data), content_type='application/json')
    client = Client.objects.get(pk=2)

    assert response.status_code == 201
    assert data['phone'] == client.phone
    assert data['mobile_code'] == client.mobile_code
    assert data['tag'] == client.tag
    assert data['time_zone'] == client.time_zone


@pytest.mark.django_db
def test_get_client(client_api, create_client):
    response = client_api.get('/api/v1/client/3/', content_type='application/json')
    data = response.data

    assert response.status_code == 200
    assert data == {
        'id': 3,
        'phone': '+79221119900',
        'mobile_code': '922',
        'tag': 'CH',
        'time_zone': 'Europe/Moscow'
    }


@pytest.mark.django_db
def test_update_client(create_client, client_api):
    data_client = {'tag': 'WR'}
    response = client_api.patch('/api/v1/client/4/', data=json.dumps(data_client), content_type='application/json')
    data = response.data

    assert response.status_code == 200
    assert data == {
        'id': 4,
        'phone': '+79221119900',
        'mobile_code': '922',
        'tag': 'WR',
        'time_zone': 'Europe/Moscow'
    }


@pytest.mark.django_db
def test_delete_client(create_client, client_api):
    response = client_api.delete('/api/v1/client/5/', content_type='application/json')

    assert response.status_code == 204
    assert not response.data


@pytest.mark.django_db
def test_get_notifications(client_api, create_notification):
    response = client_api.get('/api/v1/notification/', content_type='application/json')
    data = dict(response.data['results'][0])
    data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert data['count_status'] == 0
    assert data['id'] == 1
    assert data['id_notification'] == []
    assert data['start_date'].date() == datetime.now().date()
    assert data['start_date'].time().hour == datetime.now().hour
    assert data['start_date'].time().minute == datetime.now().minute


@pytest.mark.django_db
def test_get_notification(client_api, create_notification):
    response = client_api.get('/api/v1/get_notification/2/', content_type='application/json')
    data = response.data
    data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')

    assert response.status_code == 200
    assert data['id'] == 2
    assert data['url'] == '/api/v1/get_notification/2/'
    assert data['id_notification'] == []
    assert data['text'] == 'test'
    assert data['filter'] == 'CH'
    assert data['start_date'].date() == datetime.now().date()
    assert data['start_date'].time().hour == datetime.now().hour
    assert data['start_date'].time().minute == datetime.now().minute
    assert data['end_date'].date() == datetime.now().date() + timedelta(days=1)
    assert data['end_date'].time().hour == datetime.now().hour
    assert data['end_date'].time().minute == datetime.now().minute


@pytest.mark.django_db
def test_create_notification(client_api):
    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    data = {
        'text': 'test1',
        'filter': 'WR',
        'start_date': datetime.now().strftime(datetime_format),
        'end_date': (datetime.now() + timedelta(days=1)).strftime(datetime_format)
    }
    response = client_api.post('/api/v1/notification/create/', data=json.dumps(data), content_type='application/json')
    notification = Notification.objects.get(pk=3)

    data['start_date'] = datetime.strptime(data['start_date'], datetime_format)
    data['end_date'] = datetime.strptime(data['end_date'], datetime_format)

    assert response.status_code == 201
    assert data['text'] == notification.text
    assert data['filter'] == notification.filter
    assert data['start_date'].date() == notification.start_date.date()
    assert data['start_date'].hour == notification.start_date.hour
    assert data['start_date'].minute == notification.start_date.minute
    assert data['end_date'].date() == notification.end_date.date()
    assert data['end_date'].hour == notification.end_date.hour
    assert data['end_date'].minute == notification.end_date.minute


@pytest.mark.django_db
def test_upgrade_notification(client_api, create_notification):
    data_notification = {'text': 'upgrade text'}
    response = client_api.patch('/api/v1/notification/4/', data=json.dumps(data_notification),
                                content_type='application/json')
    data = response.data

    assert response.status_code == 200
    assert data['id'] == 4
    assert data['text'] == 'upgrade text'


@pytest.mark.django_db
def test_delete_notification(client_api, create_notification):
    response = client_api.delete('/api/v1/notification/5/', content_type='application/json')

    assert response.status_code == 204
    assert not response.data


@pytest.mark.django_db
def test_get_messages(client_api, create_client, create_notification):
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    response = client_api.get('/api/v1/message/', content_type='application/json')
    data = response.data['results'][0]

    data['create_date'] = datetime.strptime(data['create_date'], datetime_format)

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert data['id'] == 1
    assert data['create_date'].date() == datetime.now().date()
    assert data['create_date'].hour == datetime.now().hour
    assert data['create_date'].minute == datetime.now().minute
    assert data['status'] == 'No Sent'
    assert data['id_notification'] == 6
    assert data['id_client'] == 6


@pytest.mark.django_db
def test_get_message(client_api, create_client, create_notification):
    datetime_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    response = client_api.get('/api/v1/message/2/', content_type='application/json')
    data = response.data

    data['create_date'] = datetime.strptime(data['create_date'], datetime_format)

    assert response.status_code == 200
    assert data['id'] == 2
    assert data['create_date'].date() == datetime.now().date()
    assert data['create_date'].hour == datetime.now().hour
    assert data['create_date'].minute == datetime.now().minute
    assert data['status'] == 'No Sent'
    assert data['id_notification'] == 7
    assert data['id_client'] == 7
