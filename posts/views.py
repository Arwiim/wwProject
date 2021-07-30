"""Views for the post
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

# Create your views here.


class PostListViews(ListView):
    """Post view"""

    model = Post
    context_object_name = 'posts'
    template_name = 'posts/lists_posts.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create View"""

    model = Post
    template_name = 'posts/create_post.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:lists_posts')

    def form_valid(self, form):
        """Form Valid"""
        form.instance.user = self.request.user
        return super().form_valid(form)
