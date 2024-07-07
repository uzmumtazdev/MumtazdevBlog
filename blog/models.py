from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=300)
    summary = models.CharField(max_length=500)
    body = RichTextField()
    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
    tag = models.ManyToManyField(Tag)
    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)
    on_top = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.value)

class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment
