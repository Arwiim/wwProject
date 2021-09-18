"""Urls
"""
from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListViews.as_view(), name='lists_posts'),
    path('results/', views.Search.as_view(), name='search'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('detail/<slug:slug>/', views.DetailPostView.as_view(), name='detail_post'),
    path('edit/<slug:slug>/', views.EditPostView.as_view(), name='edit_post'),
    path('category/<category>/', views.PostByCategory.as_view(), name='post_by_category'),
]
