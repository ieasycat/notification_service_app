from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from main.models import Notification, Client, Message


class MessageSerializer(ModelSerializer):
    """Статусы сообщений для вывода в статистике"""
    class Meta:
        model = Message
        fields = ['pk', 'status']


class MessageDetailSerializer(ModelSerializer):
    """Вывод детальной информации о сообщении"""
    class Meta:
        model = Message
        fields = '__all__'


class ClientSerializer(ModelSerializer):
    """Отображение всех клиентов и CRUD"""
    class Meta:
        model = Client
        fields = '__all__'


class NotificationSerializer(ModelSerializer):
    """Создание, обновление и удаление рассылки"""

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationsSerializer(ModelSerializer):
    """Вывод всех рассылок"""
    id_notification = MessageSerializer(read_only=True, many=True)
    count_status = SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'start_date', 'count_status', 'id_notification']

    @staticmethod
    def get_count_status(obj):
        return obj.id_notification.count()


class NotificationDetailSerializer(ModelSerializer):
    """Вывод детальной информации о рассылке"""
    url = CharField(source='get_absolute_url', read_only=True)
    id_notification = MessageDetailSerializer(many=True)

    class Meta:
        model = Notification
        fields = '__all__'
