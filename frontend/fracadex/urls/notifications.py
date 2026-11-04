from django.urls import path
from fracadex.views.notification import notification_page, mark_notification_read, mark_all_notifications_read, delete_notification

urlpatterns = [
    path("", notification_page, name="notifications"),
    path("read/<int:notification_id>/", mark_notification_read, name="mark_notification_read"),
    path("read-all/", mark_all_notifications_read, name="mark_all_notifications_read"),
    path("delete/<int:notification_id>/", delete_notification, name="delete_notification"),
]