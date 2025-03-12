from datetime import datetime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .filters import PostFilter
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Author(ListView):
    name = 'name'
    model = Post
    context_object_name = "Posts"
    template_name = 'news.html'
    paginate_by = 3


    def get_queryset(self):
        return Post.objects.all().order_by('-dataCreations')

    def news_search(request):
        posts = Post.objects.all()
        post_filter = PostFilter(request.GET, queryset=posts)
        return render(request, 'news/news_search.html', {'filter': post_filter})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = 'Новости на следующей неделе'
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = "Posts"
    template_name = 'post.html'



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')