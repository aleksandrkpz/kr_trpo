# Файл: service_stat/config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Вместо 'stat.urls' пишем 'app_stat.urls'
    path('stat/', include('app_stat.urls')), 
]