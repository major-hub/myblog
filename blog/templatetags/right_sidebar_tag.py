from django import template
from django.db.models import Count
from blog.models import Category, Tag, Post

from django.core.cache import cache

register = template.Library()


@register.inclusion_tag('blog/categories_tpl.html')
def show_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('posts'))
        cache.set('categories', categories, (2 * 60))
    return {'categories': categories}


@register.inclusion_tag('blog/tag_tpl.html')
def show_tags():
    tags = cache.get('tags')
    if not tags:
        tags = Tag.objects.all()
        cache.set('tags', tags, (2 * 60))
    return {'tags': tags}


@register.inclusion_tag('blog/popular_tpl.html')
def show_popular(cnt=3):
    popular_posts = cache.get('popular_posts')
    if not popular_posts:
        popular_posts = Post.objects.filter(is_published=True).annotate(
            cnt=Count('comments')).order_by('-views').select_related('author')[:cnt]
        cache.set('popular_posts', popular_posts, (2 * 60))
    return {'popular_posts': popular_posts}
