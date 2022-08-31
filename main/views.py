from rest_framework import generics
from django.db.models import Prefetch
from main.serializers import *
from main.models import Notification, Client, Message


class ClientsAPIList(generics.ListCreateAPIView):
    """Просмотр клиентов и создание"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(mobile_code=serializer.validated_data['phone'][2:5])


class ClientAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Просмтр, обновление и удаление клиента"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class NotificationAPIList(generics.ListAPIView):
    """Вывод всех рассылок"""
    queryset = Notification.objects.all()
    serializer_class = NotificationsSerializer


class NotificationAPICreateView(generics.CreateAPIView):
    """Создание рассылки"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationAPIDetailView(generics.RetrieveAPIView):
    """Вывод детальной информации о рассылке"""
    queryset = Notification.objects.prefetch_related(
        Prefetch('id_notification', queryset=Message.objects.order_by('status')))
    serializer_class = NotificationDetailSerializer


class NotificationAPIUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    """Редактирование и удаление рассылки"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class MessagesAPIList(generics.ListAPIView):
    """Вывод всех сообщений"""
    queryset = Message.objects.all().order_by('-create_date')
    serializer_class = MessageDetailSerializer


class MessageAPIDetailView(generics.RetrieveAPIView):
    """Вывод детальной информации о сообщении"""
    queryset = Message.objects.all()
    serializer_class = MessageDetailSerializer
