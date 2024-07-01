from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .models import Category, Post, User, Comment
from blog.constants import POSTS_BY_PAGE
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm, EditProfileForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 
from django.db.models import Count


def filter_posts(post_objects):
    return post_objects.filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True
    ).select_related('author', 'location', 'category')


def index(request):
    posts = filter_posts(Post.objects)[:POSTS_BY_PAGE]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        post=get_object_or_404(filter_posts(Post.objects), id=id)
    comments = post.comments.order_by('created_at')
    form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'comments': comments})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = filter_posts(category.posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(
        request,
        'blog/category.html',
        {'category': category, 'page_obj': page_obj}
    )

def profile(request, username):
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
    return render(request, 'blog/profile.html', context)

@login_required
def create_post(request, post_id=None):
    if post_id is not None:
        instance = get_object_or_404(Post, id=post_id)
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None    
    form = PostForm(request.POST or None,  files=request.FILES or None, instance=instance)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})

def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('blog:profile',  username=user.username)
        else:
            form = EditProfileForm(instance=user)
        return render(request, 'blog/user.html', {'form': form})

@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = PostForm(instance=instance)
    context = {'form': form}
    if instance.author != request.user:
        # Здесь может быть как вызов ошибки, так и редирект на нужную страницу.
        raise PermissionDenied
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('blog:index')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'blog/create.html', context)

@login_required
def add_comment(request, post_id):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    post = get_object_or_404(Post, id=post_id)
    # Функция должна обрабатывать только POST-запросы.
    form = CommentForm(request.POST or None)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        comment = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        comment.author = request.user
        # В поле birthday передаём объект дня рождения.
        comment.post = post
        # Сохраняем объект в БД.
        comment.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('blog:post_detail', id =post_id)

@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment) 
    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})
    

def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment})