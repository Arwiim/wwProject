"""Urls
"""
from django.urls import path

from . import views

app_name = 'nytnews'

urlpatterns = [
    path('world/', views.WorldViewList, name='lists_news'),
]
