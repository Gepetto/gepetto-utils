from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def domain(url):
    if url:
        domain_name = '.'.join(url.split('/')[2].split('.')[-3:])
        return mark_safe(f'<a href="{url}">{domain_name}</a>')
    return '?'
