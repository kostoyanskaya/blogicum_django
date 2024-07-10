from django.db.models import Count
from django.utils.timezone import now
from django.core.paginator import Paginator

from blog.constants import COUNT_POSTS
from .models import Post


def filter_by_date(manager=Post.objects):
    return manager.filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True
    )


def annotate_with_comments(manager=Post.objects):
    return manager.annotate(
        comment_count=Count('comments')).select_related(
        'author', 'category', 'location').order_by(
        '-pub_date'
    )


def post_paginator(request, item, num=COUNT_POSTS):
    paginator = Paginator(item, num)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
