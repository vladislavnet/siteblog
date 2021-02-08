from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView
from django.db.models import F
from .models import *
from .forms import *

class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_popular_post'] = Post.objects.order_by('-views').first()
        context['title'] = 'ProgBlog'
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_popular_post'] = Post.objects.filter(category__slug=self.kwargs['slug']).order_by('-views').first()
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.get_comments.all()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

class PostByTags(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' +  str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

def comment_post(request):
    if not request.method == "POST":
        return Http404()

    form = PostCommentForm(request.POST)
    if form.is_valid():
        post = get_object_or_404(Post, pk=form.cleaned_data["post_id"])
        PostComment(
            post=post,
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            comment=form.cleaned_data["comment"]
        ).save()
        return redirect(post.get_absolute_url())
    print(form.cleaned_data["name"])
    print(form.cleaned_data["email"])
    print(form.cleaned_data["comment"])
    print(form.cleaned_data["post_id"])
    return redirect(post.get_absolute_url())