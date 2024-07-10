from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import NewsFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.utils.text import slugify

class ListNewsView(ListView):
    model = Post
    paginate_by = 10
    template_name = "news_list.html"
    context_object_name = "all_news"

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetailNewsView(DetailView):
    model = Post
    template_name = "news_detail.html"
    context_object_name = "news_detail"



class CreateNewsView(CreateView):
    model = Post
    template_name = "create_news.html"
    fields = ['title', 'text', 'categories', 'author']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slugify(instance.title)

        # Ensure the slug is unique
        unique_slug = instance.slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{instance.slug}-{num}'
            num += 1
        instance.slug = unique_slug

        instance.save()
        return super().form_valid(form)


class CreateArticleView(CreateView):
    model = Post
    template_name = 'create_article.html'
    fields = ['title', 'text', 'categories', 'author']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

class UpdateNewsView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_news.html'
    success_url = reverse_lazy('news_list')

class UpdateArticleView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_article.html'
    success_url = reverse_lazy('news_list')

class DeleteNewsView(DeleteView):
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')

class DeleteArticleView(DeleteView):
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('news_list')