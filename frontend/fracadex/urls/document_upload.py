from django.urls import path
from fracadex.views.login import upload_document

urlpatterns = [
    path("", upload_document, name="upload_document"),
]