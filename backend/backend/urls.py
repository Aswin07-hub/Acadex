

from django.contrib import admin
from django.urls import path

from beacadex import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/csrf/", views.get_csrf_token, name="csrf_token"),

    # Root URL displays student JSON data
    path("", views.register_view, name="students"),

    # Registration API
    path("api/register/", views.register_view, name="register"),

    path("api/login/", views.login_view, name="login"),

    path("api/logout/", views.logout_view, name="logout"),

    path("api/notifications/", views.notification_list, name="notification-list"),
    
    path("api/notifications/read/<int:notification_id>/", views.mark_notification_read, name="mark-notification-read"),
    
    path("api/notifications/read-all/", views.mark_all_notifications_read, name="mark-all-notifications-read"),
    
    path("api/notifications/delete/<int:notification_id>/", views.delete_notification, name="delete-notification"),
]
