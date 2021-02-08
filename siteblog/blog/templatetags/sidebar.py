from django import template
from blog.models import Post, Tag

register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(count=3)
    posts = Post.objects.order_by('-views')[:count]
    return {'posts': posts}