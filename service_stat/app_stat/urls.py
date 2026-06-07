
from django.urls import path
from . import views

urlpatterns = [ # Вызов функции при запросе по API
    path('api/get_stats/', views.get_analytics, name='get_analytics'),
]