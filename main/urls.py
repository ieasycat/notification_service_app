from django.urls import path
from main import views


urlpatterns = [
    path('client/', views.ClientsAPIList.as_view(),
         name='clients_list'),
    path("client/<int:pk>/", views.ClientAPIDetailView.as_view(),
         name='detail_client'),
    path('notification/', views.NotificationAPIList.as_view(),
         name='notifications_list'),
    path('notification/create/', views.NotificationAPICreateView.as_view(), name='create notification'),
    path('get_notification/<int:pk>/', views.NotificationAPIDetailView.as_view(),
         name='detail_notification'),
    path('notification/<int:pk>/',
         views.NotificationAPIUpdateDestroyView.as_view(), name='update_and_destroy_notification'),
    path('message/', views.MessagesAPIList.as_view(),
         name='messages_list'),
    path("message/<int:pk>/", views.MessageAPIDetailView.as_view(),
         name='detail_message'),
]
