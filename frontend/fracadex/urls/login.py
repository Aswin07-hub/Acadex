
from django.contrib import admin
from django.urls import path

from fracadex.views.login import *

urlpatterns = [
    # Login and Registration
    path('', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),

    # Student Dashboard
    path('student/dashboard/',student_dashboard, name='student_dashboard'),

    # Logout
    # path('logout/',LogoutView.as_view(), name='logout'),

    # Document Upload
    path('upload-document/', upload_document, name='upload_document'),
]