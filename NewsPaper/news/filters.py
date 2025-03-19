from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author
from django import forms


class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='iregex', label='По названию')

    author = ModelChoiceFilter(
        field_name='author',
        queryset= Author.objects.all(),
        label='По автору',
        empty_label= 'Все авторы'
    )
    dataCreations__gt =DateFilter(
        field_name='dataCreations',
        lookup_expr='gt',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )