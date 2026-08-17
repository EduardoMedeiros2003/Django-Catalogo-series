from django.urls import path
from .views import criar_serie

urlpatterns = [
    path('series', criar_serie)
]