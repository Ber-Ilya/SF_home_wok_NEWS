from django.urls import path
from .views import *

urlpatterns = [
    path('', ListNewsView.as_view(), name='news_list'),
    path('<int:pk>/', DetailNewsView.as_view(), name='news_detail'),  # Детали новости
    path('news/create/', CreateNewsView.as_view(), name='create_news'),
    path('news/<int:pk>/edit/', UpdateNewsView.as_view(), name='edit_news'),
    path('news/<int:pk>/delete/', DeleteNewsView.as_view(), name='delete_news'),
    path('articles/create/', CreateArticleView.as_view(), name='create_article'),
    path('articles/<int:pk>/edit/', UpdateArticleView.as_view(), name='edit_article'),
    path('articles/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),

]
