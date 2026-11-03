"""
URL configuration for frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from fracadex import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login and Registration
    path('', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),

    # Student Dashboard
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # Logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Document Upload
    path('upload-document/', views.upload_document, name='upload_document'),
]
