from django.urls import path
from . import views

urlpatterns = [
    # Главная страница (инфомат или ПК врача в зависимости от сессии)
    path('', views.dashboard_page, name='dashboard_page'),
    
    # Ссылка для входа под админом (ПК врача)
    path('login-admin/', views.login_as_admin, name='login_as_admin'),
    
    # Ссылка для выхода (возврат к режиму инфомата)
    path('logout/', views.logout_user, name='logout_user'),
]