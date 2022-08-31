from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Notification, Client, Message
from main.tasks import send_notification


@receiver(post_save, sender=Notification, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if kwargs:
        notification = Notification.objects.filter(id=instance.pk).first()
        clients = Client.objects.filter(tag=notification.filter).all()
        for client in clients:
            Message.objects.create(
                status="No Sent",
                id_notification=instance,
                id_client=client
            )
            message = Message.objects.filter(
                id_notification=notification.id, id_client=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone.__dict__,
                "text": notification.text
            }
            notification_id = notification.id
            client_id = client.id
            send_notification.apply_async((notification_id, client_id, data))
