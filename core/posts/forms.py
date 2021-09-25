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


class EmailPostForm(forms.Form):
    """[summary]

    Args:
        forms ([type]): [description]
    """

    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_email(self, post_id):

        # cd = self.cleaned_data
        # post_url = request.build_absolute_uri(post.get_absolute_url())

        # subject = f"{cd['name']} recommends you read " f"{post.title}"
        # message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
        # send_mail(subject, message, 'admin@myblog.com', [cd['to']])
        # print(data)
        # return data
        return []
