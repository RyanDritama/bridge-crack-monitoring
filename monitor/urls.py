
"""monitor app urls"""
from django.urls import path
from .monitor import Monitor
urlpatterns = [
     path('', Monitor.as_view(), name='home'),
]
