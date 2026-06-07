
from django.contrib import admin
from django.urls import path, include  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('input/', include('app_input.urls')), 
]