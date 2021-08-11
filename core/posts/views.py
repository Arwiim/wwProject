"""Views for the post
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.base import View
from .models import Post, Favorites
from .forms import PostForm

# Create your views here.


class PostListViews(ListView):
    """Post view"""

    model = Post
    context_object_name = 'posts'
    template_name = 'posts/lists_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['first'] = Post.objects.first()
        return context


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


class DetailPostView(DetailView):

    model = Post
    template_name = 'posts/detail_post.html'
    context_object_name = 'post'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     print(context['now'])
    #     return context


class EditPostView(LoginRequiredMixin, UpdateView):

    model = Post
    template_name = 'posts/edit_post.html'
    form_class = PostForm
    context_object_name = 'post'
    success_url = reverse_lazy('posts:lists_posts')


class Search(ListView):
    models = Post
    context_object_name = 'posts'
    template_name = 'posts/search_post.html'

    def get_queryset(self):
        key_word = self.request.GET.get('kword', '')
        return Post.objects.list_books(key_word)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kword'] = self.request.GET.get('kword', '')
        return context


# Favorites View
class AddFavorites(View):
    def post(self, request, *arg, **kwargs):
        # User
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        #
        Favorites.objects.create(user=user, post=post)

        return HttpResponseRedirect(reverse('/'))
