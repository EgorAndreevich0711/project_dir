# news/admin.py
from django.contrib import admin
from .models import Category, Post, PostCategory
from django.utils.translation import gettext_lazy as _

class PostCategoryInline(admin.TabularInline): # Или StackedInline
    model = PostCategory
    extra = 1  # Количество пустых форм для добавления связей

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_categories', 'dateCreation')
    list_filter = ('postCategory',) # Фильтруем по имени категории через PostCategory
    search_fields = ('title', 'text')
    date_hierarchy = 'dateCreation'
    ordering = ('-dateCreation',)
    inlines = [PostCategoryInline]  # Добавляем возможность редактировать связи

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.postCategory.all()]) # Отображаем имена категорий

    get_categories.short_description = 'Categories' #Подпись для колонки

admin.site.register(Category)
