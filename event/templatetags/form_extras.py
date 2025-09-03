# your_app/templatetags/form_extras.py
from django import template

register = template.Library()

@register.filter
def add_attributes(field, attributes):
    """Adds multiple attributes to a field."""
    attrs = {}
    if not hasattr(field, 'as_widget'):
        return field  # Return the field as is if it's not a form field

    for attr in attributes.split(","):
        key, value = attr.split(":")
        attrs[key.strip()] = value.strip()
    
    return field.as_widget(attrs=attrs)

@register.filter
def add_class(field, css_class):
    """Adds a CSS class to a field."""
    return add_attributes(field, f'class:{css_class}')
