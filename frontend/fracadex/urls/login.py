
from django.contrib import admin
from django.urls import path
from fracadex.views.help_support import (
    help_support_page,
    send_support_message,
    support_history
)
from fracadex.views.login import *

urlpatterns = [
    # Login and Registration
    path('', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),

    # Student Dashboard
    path('student/dashboard/',student_dashboard, name='student_dashboard'),

    # Logout
    path('logout/', logout_page, name='logout'),

    # Document Upload
    path('upload-document/', upload_document, name='upload_document'),


    path("student/help-support/", help_support_page, name="help_support"),
    path("student/help-support/send/", send_support_message, name="send_support_message"),
    path("student/help-support/history/", support_history, name="support_history"),
]