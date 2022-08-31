from django.contrib import admin
from .models import Notification, Client, Message


admin.site.register(Notification)
admin.site.register(Client)
admin.site.register(Message)
