# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:post_id>/', views.news_detail, name='news_detail'),
    # другие URL-адреса
]
