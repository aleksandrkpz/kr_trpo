from django.urls import path
from . import views 


urlpatterns = [
    # вызов функции при запросе по API
    path('api/diseases/', views.api_get_diseases, name='api_diseases'),
    path('api/humans/create/', views.api_create_human, name='api_create_human'),
    path('api/humans/list/', views.api_get_humans_data, name='api_humans_list'),
]