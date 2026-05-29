from django.urls import path
from .views import output_page

urlpatterns = [
    path('', output_page, name='output_page'),
]
