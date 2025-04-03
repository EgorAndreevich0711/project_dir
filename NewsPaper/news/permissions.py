from django.contrib.auth.models import Group
from django.contrib.auth.mixins import  UserPassesTestMixin
from django.shortcuts import redirect


class AuthorRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return redirect('signup')
        else:
            return redirect('login')
