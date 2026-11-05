
from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),

    # Login, Registration, Student and HOD pages
    path('', include('fracadex.urls.login')),

    # Other modules
    path('profile/', include('fracadex.urls.profile')),

    path(
        'notifications/',
        include('fracadex.urls.notifications')
    ),

]
