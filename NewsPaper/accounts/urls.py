# urls.py (напр., в приложении `accounts`)
from django.urls import path
from . import views

urlpatterns = [
    # ... другие URL ...
    path('news_button/', views.news_button_page, name='news_button_page'),
    # ...
]