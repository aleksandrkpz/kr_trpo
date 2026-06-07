# Файл: service_main/config/urls.py
from django.contrib import admin
from django.urls import path, include # <-- проверь импорт include

urlpatterns = [
    path('admin/', admin.site.urls), # <-- тут исправил на urls
    # Говорим, что по адресу /main/ нужно искать урлы внутри приложения main
    path('', include('app_main.urls')), 
]