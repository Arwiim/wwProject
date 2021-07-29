"""Urls
"""
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListViews.as_view(), name='lists_posts'),
    path('create', views.PostCreateView.as_view(), name='create_post'),
]
