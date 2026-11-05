
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from beacadex import views

from beacadex.request_views import submission_requests_api
from beacadex.hod_document_views import hod_documents_api

from beacadex.document_views import (
    upload_student_document,
    student_documents_api,
    edit_student_document,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("api/csrf/", views.get_csrf_token, name="csrf_token"),
    path("", views.register_view, name="students"),
    path("api/register/", views.register_view, name="register"),
    path("api/login/", views.login_view, name="login"),
    path("api/logout/", views.logout_view, name="logout"),

    # Student Profile
    path(
        "api/student-profile/",
        include("beacadex.urls.profile")
    ),

    # HOD Submission Requests
    path(
        "api/submission-requests/",
        submission_requests_api,
        name="submission_requests_api"
    ),

    # HOD Document Review
    path(
        "api/hod/documents/",
        hod_documents_api,
        name="hod_documents_api"
    ),

    # Student Documents
    path(
        "api/documents/upload/",
        upload_student_document,
        name="upload_student_document"
    ),

    path(
        "api/documents/",
        student_documents_api,
        name="student_documents_api"
    ),

    path(
        "api/documents/edit/",
        edit_student_document,
        name="edit_student_document"
    ),
]

# Serve uploaded files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
