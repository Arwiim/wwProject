"""Forms
"""
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form definition for Post"""

    class Meta:
        """Meta difinition"""

        model = Post
        fields = ('title', 'image_header', 'post', 'is_draft', 'categories')


class CommentForm(forms.ModelForm):
    """Form definition for Post"""

    class Meta:
        """Meta difinition"""

        model = Comment
        fields = ('name', 'email', 'body')
