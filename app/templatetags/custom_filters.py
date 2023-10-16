from django import template

register = template.Library()

@register.filter
def get_extension(value):
    # Assuming value is a file path or content type
    parts = value.split('.')
    if len(parts) > 1:
        return parts[-1]
    return ''
