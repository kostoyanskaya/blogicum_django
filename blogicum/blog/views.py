from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from .services import annotate_with_comments, filter_by_date, post_paginator
from .models import Category, Comment, Post, User
from .forms import CommentForm, EditProfileForm, PostForm


class RegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


def index(request):
    posts = annotate_with_comments(filter_by_date(Post.objects))
    page_obj = post_paginator(request, posts)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(filter_by_date(Post.objects), id=post_id)
    comments = post.comments.all().select_related('author',)
    return render(request, 'blog/detail.html', {
        'post': post, 'comments': comments, 'form': CommentForm()
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = annotate_with_comments(
        filter_by_date(category.posts)
    )
    page_obj = post_paginator(request, posts)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts_list = annotate_with_comments(profile.posts.all())
    if not request.user == profile:
        posts_list = filter_by_date(posts_list)

    page_obj = post_paginator(request, posts_list)
    return render(
        request,
        'blog/profile.html',
        {'profile': profile, 'page_obj': page_obj}
    )


@login_required
def create_post(request, post_id=None):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_profile(request):
    author = request.user
    if author != request.user:
        return redirect('blog:profile', request.user)
    form = EditProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    form = PostForm(instance=instance)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=instance)
        instance.delete()
        return redirect('blog:index')

    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request, 'blog/comment.html', {'form': form, 'comment': comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'comment': comment})
