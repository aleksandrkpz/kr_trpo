
from django.urls import path
from . import views

urlpatterns = [
    path('api/get_stats/', views.get_analytics, name='get_analytics'),
]