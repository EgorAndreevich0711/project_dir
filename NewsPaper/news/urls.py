from django.urls import path

from .views import *

app_name = 'news'

urlpatterns = [
    path('', News.as_view(), name='post_list'),
    path('categories/<int:category_id>/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post'),
    path('search/', news_search, name='post_search'),
    path('news/create/', PostCreate.as_view(), {'post_type': 'news'}, name='create_news'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), {'post_type': 'articles'}, name='create_article'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('categories/<int:category_id>/subscribe', subscribe, name='subscribe'),

]