from django.urls import reverse
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from notification_service.settings import TIME_ZONES


class Tag(models.TextChoices):
    CHILD = 'CH'
    SCHOOLBOY = 'SC'
    STUDENT = 'ST'
    WORKER = 'WR'
    RETIREE = 'RT'


class Notification(models.Model):
    text = models.CharField(max_length=1000)
    filter = models.CharField(choices=Tag.choices, max_length=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('detail notification', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.start_date}'

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class Client(models.Model):
    phone = PhoneNumberField(unique=True, region='RU')
    mobile_code = models.CharField(max_length=3)
    tag = models.CharField(
        choices=Tag.choices, max_length=2)
    time_zone = models.CharField(
        choices=TIME_ZONES, max_length=32)

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    class Status(models.TextChoices):
        Success = 'Success'
        Waiting = 'Waiting'
        No_Sent = 'No Sent'
        Error = 'Error'
        Wrong_Time = 'Wrong Time'

    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, max_length=10)
    id_notification = models.ForeignKey(
        Notification, on_delete=models.DO_NOTHING, related_name='id_notification')
    id_client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, related_name='to_client')

    def __str__(self):
        return f'{self.id_client}, {self.status} {self.create_date}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
