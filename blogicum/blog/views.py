from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.shortcuts import redirect

from .models import Category, Comment, Post, User
from .forms import CommentForm, EditProfileForm, PostForm


def filter_posts(post_objects):
    return post_objects.filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True
    ).select_related('author', 'location', 'category').annotate(
        comment_count=Count('comments')
    )


def index(request):
    posts = filter_posts(Post.objects).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        post = get_object_or_404(filter_posts(Post.objects), id=id)
    comments = post.comments.order_by('created_at')
    form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'form': form,
                                                'comments': comments})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = filter_posts(category.posts).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )


def profile(request, username):
    template = 'blog/profile.html'
    user = get_object_or_404(User, username=username)
    posts_list = (
        user.posts
        .annotate(comment_count=Count('comments'))
        .order_by('-pub_date')
    )
    paginator = Paginator(posts_list, 10)
    num_pages = request.GET.get('page')
    page_obj = paginator.get_page(num_pages)
    context = {'profile': user, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def create_post(request, post_id=None):
    if request.method == 'POST':
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
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_profile(request):
    template = 'blog/user.html'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', request.user)
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=instance)
    context = {'form': form}
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=instance)
        instance.delete()
        return redirect('blog:index')

    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return (redirect('blog:post_detail', post_id))
    if request.method == "POST":
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(
        request, 'blog/comment.html', {'form': form, 'comment': comment}
    )


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return (redirect('blog:post_detail', post_id))
    if request.method == "POST":
        comment.delete()
        return redirect('blog:post_detail', post_id)

    return render(request, 'blog/comment.html', {'comment': comment})
