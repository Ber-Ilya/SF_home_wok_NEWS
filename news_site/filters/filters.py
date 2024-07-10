from django_filters import FilterSet, ModelMultipleChoiceFilter
from ..models import *

class NewsFilter(FilterSet):
    author = ModelMultipleChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Фильтр по автору',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            "text": ['icontains'],
            'created_at': ['lt'],
            'categories': ['exact'],
        }

