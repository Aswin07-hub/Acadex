# from django.contrib import admin
# from django.urls import path

# from fracadex.views.profile import *

# urlpatterns = []
from django.contrib import admin

from django.urls import path

from fracadex.views.profile import student_profile

urlpatterns = [
    path('', student_profile, name='student_profile'),
]
