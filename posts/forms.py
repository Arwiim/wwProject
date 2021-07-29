"""Forms
"""
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Form definition for Post"""

    class Meta:
        """Meta difinition"""

        model = Post
        fields = ('user', 'title', 'image_header', 'post', 'is_draft', 'categories')
