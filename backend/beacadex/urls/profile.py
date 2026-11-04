# from django.urls import path
# from beacadex.views.profile import student_profile_view

# urlpatterns = [
#     path(
#         "",
#         student_profile_view,
#         name="student_profile"
#     ),
# ]
from django.urls import path
from beacadex.profile_views.profile import student_profile_view

urlpatterns = [
    path("", student_profile_view, name="student_profile"),
]