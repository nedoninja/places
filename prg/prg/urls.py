"""
URL configuration for prg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function vie    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('check-mail/', views.check_mail, name='check_mail'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('login/', views.user_login, name='login'),
    
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create-service/', views.create_service, name='create_service'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('my_feedbacks/', views.my_feedbacks, name='my_feedbacks'),
    path('chat/', views.chat, name='chat'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)