import django_filters
from .models import Post, Author
from django.contrib.auth.models import User
from django import forms


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='По названию')
    author__authorUser__username = django_filters.CharFilter(field_name='author__authorUser__username', lookup_expr='icontains', label='По имени автора')
    dataCreations__gt = django_filters.DateFilter(field_name='dataCreations', lookup_expr='gt',label='Позже указанной даты', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author__authorUser__username', 'dataCreations__gt']
