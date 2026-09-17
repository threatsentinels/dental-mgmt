from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary and key in dictionary:
        return dictionary[key]
    return None