from django.urls import path, include
from .views import *


urlpatterns = [
    path('', Author.as_view(),name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', news_search, name='post_search'),
    path('news/create/', PostCreate.as_view(), {'post_type': 'news'}, name='create_news'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), {'post_type': 'articles'}, name='create_article'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]