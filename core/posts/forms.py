"""Forms
"""
from django import forms
from django.core.mail import send_mail
from blog.settings import DEBUG
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


class EmailPostForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """

    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self, post):

        cd = self.cleaned_data
        post_to_share = post.get_absolute_url()

        if DEBUG == 'TRUE':
            post_url = 'http://localhost:8000{path}'.format(path=post_to_share)
        else:
            post_url = 'http://mysite{path}'.format(path=post_to_share)

        subject = f"{cd['name']} recommends you read " f"{post.title}"
        message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
        send_mail(subject, message, 'arwiimm@gmail.com', [cd['to']])
