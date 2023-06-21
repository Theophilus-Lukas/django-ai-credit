"""creditaidjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from creditaidjango import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('image/all/', views.get_all_image),
    path('image/upload/', views.upload_image_data),
    path('image/delete/', views.delete_image_data),

    # feature 1
    path('ktpverification/', views.ktp_verification),

    # feature 2
    path('nib/', views.nib_extract),
    path('siup/', views.siup_extract),
    path('tdp/', views.tdp_extract),
    path('skdp/', views.skdp_extract),
    path('npwp/', views.npwp_extract),

    path('admin/', admin.site.urls),
    path('ping/', views.ping),
    path('', views.ping),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
