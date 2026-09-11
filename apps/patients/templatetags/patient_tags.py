from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieves a dictionary value by dynamic key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key) or dictionary.get(str(key)) or dictionary.get(int(key) if str(key).isdigit() else key)
    return None