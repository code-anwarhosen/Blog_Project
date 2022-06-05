from django import forms
from .models import Blog_Post, Blog_Comment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog_Post
        fields = ("title", "image", "content")

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Blog_Comment
        fields = ("comment",)

