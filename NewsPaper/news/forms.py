from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = ['author', 'title', 'text']
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return name


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='connom')
        basic_group.user_set.add(user)
        return user