from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Splits a string by the given argument."""
    return value.split(arg)