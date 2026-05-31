from django.urls import path
from.import views
# связываем начальную страницу с функцией dashboard_page
urlpatterns = [
    path('', views.dashboard_page, name='dashboard_page'), 
]