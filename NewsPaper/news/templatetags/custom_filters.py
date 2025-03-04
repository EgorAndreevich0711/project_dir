from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

CENSORED_WORDS = [
    'какашка',
    'блин',
    'херня',
]


@register.filter(name='censor')
def censor(value):
    """
    Заменяет буквы нежелательных слов в тексте на символ '*'.
    """
    text = str(value)  # Преобразуем значение в строку

    for word in CENSORED_WORDS:
        replacement = '*' * len(word)
        text = text.replace(word, replacement)

    return mark_safe(text)