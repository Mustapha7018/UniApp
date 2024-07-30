from django import template

register = template.Library()


@register.filter(name="truncate_ellipsis")
def truncate_ellipsis(value, arg):
    try:
        length = int(arg)
        if len(value) > length:
            return value[:length] + "..."
        return value
    except (ValueError, TypeError):
        return value
