from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django import forms
from .filters import PostFilter
from .forms import PostForm
from news.models import Post, Category, Author
from .permissions import AuthorRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist


class News(ListView):
    model = Post
    context_object_name = "Posts"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = 'Новости на следующей неделе'
        context['filter'] = self.filterset
        return context

    def get_template_names(self):
        if self.request.path == '/post/search':
            return 'news_search.html'
        return 'news.html'

#class PostList(ListView):
#    model = Post
#    template_name = 'news.html' # <== Убедитесь, что такой файл есть
#    context_object_name = 'posts'

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
    success_url = reverse_lazy('news:post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW' if self.kwargs.get('post_type') == 'news' else 'AR'
        if self.request.path == '/post/articles/create':
            post.categoryType = 'AR'
        #post.author = News.objects.get(authorUser= self.request.get)

        post.save()
        form.save_m2m()
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
            raise PermissionDenied
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

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'news/category_list.html', {'posts': posts})

class PostForm(forms.ModelForm):
    postCategory = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'postCategory']


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, category_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})