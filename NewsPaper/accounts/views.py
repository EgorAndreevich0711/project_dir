# views.py (напр., в приложении `accounts`)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def news_button_page(request):
    """Отображает страницу с кнопкой перехода на страницу новостей."""
    return render(request, 'accounts/news_button_page.html')
