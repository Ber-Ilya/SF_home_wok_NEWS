from django import template
import re

register = template.Library()

# Список слов, которые нужно цензурировать
CENSORED_WORDS = ["редиска", "плохой"]


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр censor может применяться только к строковым типам.")

    # Создаем шаблон регулярного выражения для поиска цензурируемых слов
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in CENSORED_WORDS) + r')\b', re.IGNORECASE)

    def replace(match):
        word = match.group()
        return word[0] + "*" * (len(word) - 1)

    return pattern.sub(replace, value)

