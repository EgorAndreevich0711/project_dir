from django.contrib.auth.models import Group
from django.contrib.auth.mixins import  UserPassesTestMixin
from django.shortcuts import redirect


class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь членом группы 'authors'.
    """
    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def handle_no_permission(self):
        # Перенаправление или другое действие, если нет прав доступа
        if self.request.user.is_authenticated:
            # Пользователь авторизован, но не является автором
            return redirect('signup')  # Перенаправление на главную или другую страницу
        else:
            # Пользователь не авторизован
            return redirect('login')  # Перенаправление на страницу входа
