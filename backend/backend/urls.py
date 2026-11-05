

from django.contrib import admin
from django.urls import path,include

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
    path("api/student-profile/", include("beacadex.urls.profile")),

    path("api/support/chat/", views.support_chat, name="support_chat"),

    path("api/support/history/", views.support_history, name="support_history"),
]
