from django import forms
from .models import *
from .filters import NewsFilter

class PostForm(forms.ModelForm):
    filter = NewsFilter()
    class Meta:
        model = Post
        fields = {
                "author",
                "title",
                "text",
                "categories",
                "created_at",
        }