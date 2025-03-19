from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import PostFilter
from .forms import PostForm
from .models import Post
from .permissions import AuthorRequiredMixin
from django.core.exceptions import PermissionDenied




class Author(ListView):
    model = Post
    context_object_name = "Posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = 'Новости на следующей неделе'
        context['filterset'] = self.filterset
        return context

    def get_template_names(self):
        if self.request.path == '/post/search':
            return 'news_search.html'
        return 'news.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = "Posts"
    template_name = 'post.html'

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def news_search(request):
    posts = Post.objects.all().order_by('-dataCreations')
    filterset = PostFilter(request.GET, queryset=posts)
    posts = filterset.qs
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'filterset': filterset
    }
    return render(request, 'news_search.html', context)


class PostCreate(CreateView,LoginRequiredMixin, AuthorRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form,):
        post = form.save(commit=False)
        post.categoryType = 'NW' if self.kwargs.get('post_type') == 'news' else 'AR'
        if self.request.path == '/post/articles/create':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)


class PostEdit(UpdateView,LoginRequiredMixin, AuthorRequiredMixin,):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('post_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = self.kwargs.get('post_type')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def form_valid(self, form):
        post = form.save()
        return redirect('post_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise PermissionDenied  # Нельзя редактировать чужие посты
        return obj



class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = self.kwargs.get('post_type')
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise PermissionDenied

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'news.html'
