from datetime import datetime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Post



class Author(ListView):
    name = 'name'
    model = Post
    context_object_name = "Posts"
    template_name = 'news.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-dataCreations')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = 'Новости на следующей неделе'
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = "Posts"
    template_name = 'post.html'



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')