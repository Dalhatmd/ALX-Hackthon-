from .views import NotificationListView, NotificationMarkAsReadView, mark_notification_as_read, mark_all_notifications_as_read
from django.urls import path


urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/read/', NotificationMarkAsReadView.as_view(), name='notification-mark-as-read'),
    path('notifications/<int:pk>/mark-as-read/', mark_notification_as_read, name='notification-mark-as-read'),
    path('notifications/mark-all-as-read/', mark_all_notifications_as_read, name='notification-mark-all-as-read')
]
