"""myhouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import  views
from django.conf import settings
from   django.conf.urls.static import  static

from rest_framework import routers


router = routers.DefaultRouter()


urlpatterns = [
    path('deido/', admin.site.urls),
    path('', views.myhouse,  name='myhouse'),
    path('login/', views.login_site, name='login'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_site,name='logout'),
    path('camhouse/', include('camhouse.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #pour les images