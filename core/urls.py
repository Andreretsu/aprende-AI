from django.urls import path
from .views import index, talk

urlpatterns = [
    path('', index),
    path('talk/', talk),
]
