from django.contrib import admin
from django.urls import path
from app_input.views import input_page  # Импортируем нашу функцию

urlpatterns = [
    path('admin/', admin.site.urls),
    path('input/', input_page),  # Вот этой строчки Django в config.urls сейчас не видит!
]
