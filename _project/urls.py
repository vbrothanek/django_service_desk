"""
URL configuration for _project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()
admin_url = os.getenv('ADMIN_URL') +'/'

urlpatterns = [
    path('',include('service_desk.urls')),
    path('accounts/', include('allauth.urls')),
    path(admin_url, admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns.extend(debug_toolbar_urls())
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
