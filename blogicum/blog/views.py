from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.shortcuts import redirect

from blog.constants import COUNT_POSTS
from .models import Category, Comment, Post, User
from .forms import CommentForm, EditProfileForm, PostForm


def filter_posts(manager=Post.objects, filters=True, annotations=True):
    test = manager.select_related(
        'author',
        'location',
        'category'
    )
    if filters:
        test = test.filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True
        )
    if annotations:
        test = test.annotate(
            comment_count=Count('comments')
    ).order_by(
        '-pub_date'
    )
    return test

def post_paginator(request, item, num=COUNT_POSTS):
    paginator = Paginator(item, num)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)

def index(request):
    posts = filter_posts(Post.objects)
    page_obj = post_paginator(request, posts)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(filter_posts(Post.objects), id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'form': CommentForm()})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = filter_posts(category.posts).order_by('-pub_date')
    page_obj = post_paginator(request, posts)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    if request.user == profile:
        posts_list = Post.objects.filter(author=request.user).annotate(
            comment_count=Count('comments')).order_by('-pub_date')
    else:
        posts_list = filter_posts().filter(author=profile)

    page_obj = post_paginator(request, posts_list)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request, post_id=None):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('blog:profile', request.user)
    else:
        form = PostForm()
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
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_profile(request):
    author = request.user
    if author != request.user:
        return redirect('blog:profile')
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
        return (redirect('blog:post_detail', post_id=post_id))
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
        return (redirect('blog:post_detail', post_id=post_id))
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'comment': comment})
