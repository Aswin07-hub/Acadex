
from django.urls import path

from fracadex.views.login import (
    login_page,
    register_page,
    student_dashboard,
    logout_page,
)

from fracadex.views.document_upload import upload_document
from fracadex.views.my_documents import my_documents_page
from fracadex.views.edit_document import edit_document_page

from fracadex.views.hod_requests import hod_requests_page
from fracadex.views.hod_documents import hod_documents_page

from fracadex.views.help_support import (
    help_support_page,
    send_support_message,
    support_history
)

urlpatterns = [
    path("", login_page, name="login_page"),

    path("register/", register_page, name="register_page"),

    path(
        "student/dashboard/",
        student_dashboard,
        name="student_dashboard"
    ),

    path(
        "upload-document/",
        upload_document,
        name="upload_document"
    ),

    path(
        "my-documents/",
        my_documents_page,
        name="my_documents_page"
    ),

    path(
        "my-documents/edit/<int:document_id>/",
        edit_document_page,
        name="edit_document_page"
    ),

    path(
        "hod/requests/",
        hod_requests_page,
        name="hod_requests_page"
    ),

    path(
        "hod/documents/",
        hod_documents_page,
        name="hod_documents_page"
    ),

    path("logout/", logout_page, name="logout"),

    path("student/help-support/", help_support_page, name="help_support"),
    path("student/help-support/send/", send_support_message, name="send_support_message"),
    path("student/help-support/history/", support_history, name="support_history"),
]
