"""Views for the post
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import View
from core.users.models import Favorites
from .models import Category, Post
from .forms import PostForm, CommentForm

# Create your views here.


class PostByCategory(ListView):

    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_by_category.html'

    def get_context_data(self, **kwargs):
        category = self.kwargs['category']
        category = Category.objects.get(name=category)
        context = super().get_context_data(**kwargs)
        context['category'] = category
        context['post_by_cat'] = Post.objects.filter(categories=category)
        return context


class PostListViews(ListView):
    """Post view"""

    model = Post
    context_object_name = 'posts'
    template_name = 'posts/lists_posts.html'

    def get_context_data(self, **kwargs):
        favorites_id = []
        if self.request.user:
            user = self.request.user
            try:
                favorites = Favorites.objects.filter(user_from=user.id)
                for fav_id in favorites:
                    favorites_id.append(fav_id.post_fav.id)
            except Exception:
                favorites_id = None
        context = super().get_context_data(**kwargs)
        context['first'] = Post.objects.first()
        context['fav'] = favorites_id

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


class DetailPostView(View):

    model = Post
    template_name = 'posts/detail_post.html'
    context_object_name = 'post'
    comment_form = CommentForm

    def get(self, request, *args, **kwargs):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        new_comment = None
        post_n = get_object_or_404(self.model, slug=kwargs['slug'])
        comments = post_n.comments.all()
        form = self.comment_form()
        return render(
            request,
            self.template_name,
            context={'comment_form': form, 'post': post_n, 'comments': comments, 'new_comment': new_comment},
        )

    def post(self, request, *args, **kwargs):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_slug = kwargs['slug']
            new_comment.post = Post.objects.get(slug=kwargs['slug'])
            new_comment.save()
            return HttpResponseRedirect(reverse('posts:detail_post', kwargs={'slug': post_slug}))

        return render(request, self.template_name, {'form': comment_form})


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
