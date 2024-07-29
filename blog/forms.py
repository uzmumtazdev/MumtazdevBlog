from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'body', 'image', 'author', 'category', 'tag', 'published', 'on_top']
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
