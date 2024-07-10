from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f'{self.user.username} (рейтинг: {self.rating})'

    def update_rating(self):
        post_ratings = sum(post.rating for post in self.post_set.all()) * 3
        comment_ratings = sum(comment.rating for comment in self.user.comment_set.all())
        post_comment_ratings = sum(comment.rating for comment in Comment.objects.filter(post__author=self))

        self.rating = post_ratings + comment_ratings + post_comment_ratings
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPE_CHOICES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()
        self.author.update_rating()

    def dislike(self):
        self.rating -= 1
        self.save()
        self.author.update_rating()

    def preview(self):
        return self.text[:124] + "..." if len(self.text) > 124 else self.text

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Категория публикации"
        verbose_name_plural = "Категории публикаций"

    def __str__(self):
        return f'{self.post.title} - {self.category.name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Комментарий от {self.user.username} к {self.post.title}'

    def like(self):
        self.rating += 1
        self.save()
        self.post.author.update_rating()

    def dislike(self):
        self.rating -= 1
        self.save()
        self.post.author.update_rating()
