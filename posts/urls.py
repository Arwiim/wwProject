"""Urls
"""
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListViews.as_view(), name='lists_posts'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('detail/<slug:slug>/', views.DetailPostView.as_view(), name='detail_post'),
]
