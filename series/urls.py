from django.urls import path
from .views import series

urlpatterns = [
    path('series', series),
]