from django import template


register = template.Library()


@register.filter(name='get')
def get(d, k):
    return getattr(d, k) if hasattr(d, k) else None
