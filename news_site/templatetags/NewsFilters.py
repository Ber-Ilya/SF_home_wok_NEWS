from django import template
from ..filters import NewsFilter  # Убедитесь, что импортируете правильно

register = template.Library()

@register.filter(name="NewsFilters")
def news_filter(queryset, request):
    return NewsFilter(request.GET, queryset).qs